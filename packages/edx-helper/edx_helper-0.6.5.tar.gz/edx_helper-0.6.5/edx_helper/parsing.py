# -*- coding: utf-8 -*-

"""
Parsing and extraction functions
"""
import sys
import re
import json

from datetime import timedelta, datetime

from bs4 import BeautifulSoup as BeautifulSoup_

from .common import Course, Section, SubSection, Block, Unit, WebpageUnit, Video

if sys.version_info[:2] >= (3, 4):
    import html
else:
    from six.moves import html_parser
    html = html_parser.HTMLParser()

# Force use of bs4 with html.parser
BeautifulSoup = lambda page: BeautifulSoup_(page, 'html.parser')


def edx_json2srt(o):
    """
    Transform the dict 'o' into the srt subtitles format
    """
    if o == {}:
        return ''

    base_time = datetime(1, 1, 1)
    output = []

    for i, (s, e, t) in enumerate(zip(o['start'], o['end'], o['text'])):
        if t == '':
            continue

        output.append(str(i) + '\n')

        s = base_time + timedelta(seconds=s/1000.)
        e = base_time + timedelta(seconds=e/1000.)
        time_range = "%02d:%02d:%02d,%03d --> %02d:%02d:%02d,%03d\n" % \
                     (s.hour, s.minute, s.second, s.microsecond/1000,
                      e.hour, e.minute, e.second, e.microsecond/1000)

        output.append(time_range)
        output.append(t + "\n\n")

    return ''.join(output)

class JsonExtractor(object):
    """
    Base class for JsonExtractor
    Every subclass can represent a different data structures from API of an OpenEdX site.
    They should implement the given methods.
    """

    def extract_courses(self, deserialized_response):
        """
        Method to extract the courses from response of courses api
        """
        raise NotImplementedError("Subclasses should implement this")

    def extract_sequential_blocks(self, deserialized_response):
        """
        Method to extract the sequential blocks from deserialized response
        """
        raise NotImplementedError("Subclasses should implement this")

    def extract_vertical_blocks(self, deserialized_response, url):
        """
        Method to extract the vertical blocks from deserialized response
        """
        raise NotImplementedError("Subclasses should implement this")

    def extract_units(self, deserialized_response):
        """
        Method to extract the units from deserialized response
        """
        raise NotImplementedError("Subclasses should implement this")

class EdXJsonExtractor(JsonExtractor):

    def extract_courses(self, response):
        """
        Extracts the courses from response of courses api
        """
        courses = []
        for item in response['courses']:
            course_id = item['courseRun']['courseId']
            course_name = item['course']['courseName']
            course_url = item['courseRun']['homeUrl']
            if item['courseRun']['isStarted']:
                course_state = 'Started'
            elif item['enrollment']['isAudit'] and not item['enrollment']['isAuditAccessExpired']:
                course_state = 'Started'
            else:
                course_state = 'Not yet'
            courses.append(Course(course_id=course_id,
                                  course_name=course_name,
                                  course_url=course_url,
                                  course_state=course_state))
        return courses

    def extract_sequential_blocks(self, response):
        """
        Extract the sequential blocks from deserialized response
        """

        def _make_children(info, ids):
            children = [Block(position=idx,
                              block_id=block_id,
                              name=all_blocks[block_id]['display_name'],
                              block_type=all_blocks[block_id]['type'],
                              url=all_blocks[block_id]['lms_web_url'],
                              children=None
                              )
                        for idx, block_id in enumerate(ids, 1)]
            return children

        all_blocks = response['course_blocks']['blocks']
        chapter_blocks = []
        for _, block in all_blocks.items():
            if block['type'] == 'course':
                chapter_block_ids = block['children']
                for i, chapter_block_id in enumerate(chapter_block_ids, 1):
                    children_ids = all_blocks[chapter_block_id]['children']
                    chapter_block = Block(position=i,
                                          block_id=chapter_block_id,
                                          name=all_blocks[chapter_block_id]['display_name'],
                                          block_type=all_blocks[chapter_block_id]['type'],
                                          url=all_blocks[chapter_block_id]['lms_web_url'],
                                          children=_make_children(all_blocks, children_ids)
                                          )
                    chapter_blocks.append(chapter_block)
        return chapter_blocks

    def extract_vertical_blocks(self, deserialized_response, EDX_LEARN_BASE_URL):
        """
        Method to extract the vertical blocks from deserialized response
        """
        sequential_block_id = deserialized_response['item_id']
        items = deserialized_response['items']
        vertical_blocks = []
        for i, item in enumerate(items, 1):
            block_id = item['id']
            url = EDX_LEARN_BASE_URL + sequential_block_id + '/' + block_id
            block = Block(position=i,
                          block_id=block_id,
                          name=item['page_title'],
                          block_type=item['type'],
                          url=url,
                          children=None,
                          )
            vertical_blocks.append(block)
        return vertical_blocks


class PageExtractor(object):
    """
    Base class for PageExtractor
    Every subclass can represent a different layout for an OpenEdX site.
    They should implement the given methods.
    """

    def extract_units_from_html(self, page, BASE_URL, file_formats):
        """
        Method to extract the resources (units) from the given page
        """
        raise NotImplementedError("Subclasses should implement this")

    def extract_sections_from_html(self, page, BASE_URL):
        """
        Method to extract the sections (and subsections) from an html page
        """
        raise NotImplementedError("Subclasses should implement this")

    def extract_courses_from_html(self, page, BASE_URL):
        """
        Method to extract the courses from an html page
        """
        raise NotImplementedError("Subclasses should implement this")


class ClassicEdXPageExtractor(PageExtractor):

    def extract_units_from_html(self, page, BASE_URL, file_formats):
        """
        Extract Units from the html of a subsection webpage as a list of
        resources
        """
        # in this function we avoid using beautifulsoup for performance reasons
        # parsing html with regular expressions is really nasty, don't do this if
        # you don't need to !
        re_units = re.compile('(<div?[^>]id="seq_contents_\d+".*?>.*?<\/div>)',
                              re.DOTALL)
        units = []

        for unit_html in re_units.findall(page):
            unit = self.extract_unit(unit_html, BASE_URL, file_formats)
            if len(unit.videos) > 0 or len(unit.resources_urls) > 0:
                units.append(unit)
        return units

    def extract_unit(self, text, BASE_URL, file_formats):
        """
        Parses the <div> of each unit and extracts the urls of its resources
        """
        video_youtube_url = self.extract_video_youtube_url(text)
        available_subs_url, sub_template_url = self.extract_subtitle_urls(text, BASE_URL)
        mp4_urls = self.extract_mp4_urls(text)
        videos = [Video(video_youtube_url=video_youtube_url,
                        available_subs_url=available_subs_url,
                        sub_template_url=sub_template_url,
                        mp4_urls=mp4_urls)]

        resources_urls = self.extract_resources_urls(text, BASE_URL,
                                                     file_formats)
        return Unit(videos=videos, resources_urls=resources_urls)

    def extract_video_youtube_url(self, text):
        re_video_youtube_url = re.compile(r'data-streams=&#34;.*?1.0\d+\:(?:.*?)(.{11})')
        video_youtube_url = None
        match_video_youtube_url = re_video_youtube_url.search(text)

        if match_video_youtube_url is None:
            re_video_youtube_url = re.compile(r'https://www.youtube.com/embed/(.{11})\?rel=')
            match_video_youtube_url = re_video_youtube_url.search(text)

        if match_video_youtube_url is not None:
            video_id = match_video_youtube_url.group(1)
            video_youtube_url = 'https://youtube.com/watch?v=' + video_id

        return video_youtube_url

    def extract_subtitle_urls(self, text, BASE_URL):
        re_sub_template_url = re.compile(r'data-transcript-translation-url=(?:&#34;|")([^"&]*)(?:&#34;|")')
        re_available_subs_url = re.compile(r'data-transcript-available-translations-url=(?:&#34;|")([^"&]*)(?:&#34;|")')
        available_subs_url = None
        sub_template_url = None
        match_subs = re_sub_template_url.search(text)

        if match_subs:
            match_available_subs = re_available_subs_url.search(text)
            if match_available_subs:
                available_subs_url = BASE_URL + match_available_subs.group(1)
                sub_template_url = BASE_URL + match_subs.group(1) + "/%s"

        else:
            re_available_subs_url=re.compile(r'href=(?:&#34;|")([^"&]+)(?:&#34;|")&gt;Download transcript&lt;')
            match_available_subs = re_available_subs_url.search(text)
            if match_available_subs:
                sub_template_url = BASE_URL + match_available_subs.group(1)
                available_subs_url = None

        return available_subs_url, sub_template_url

    def extract_mp4_urls(self, text):
        """
        Looks for available links to the mp4 version of the videos
        """
        # mp4 urls may be in two places, in the field data-sources, and as <a>
        # refs This regex tries to match all the appearances, however we
        # exclude the ';' # character in the urls, since it is used to separate
        # multiple urls in one string, however ';' is a valid url name
        # character, but it is not really common.
        re_mp4_urls = re.compile(r'(?:(https?://[^;]*?\.mp4))')
        mp4_urls = list(set(re_mp4_urls.findall(text)))

        return mp4_urls

    def extract_resources_urls(self, text, BASE_URL, file_formats):
        """
        Extract resources looking for <a> references in the webpage and
        matching the given file formats
        """
        formats = '|'.join(file_formats)
        re_resources_urls = re.compile(r'&lt;a href=(?:&#34;|")([^"&]*.(?:' + formats + '))(?:&#34;|")')
        resources_urls = []
        for url in re_resources_urls.findall(text):
            if url.startswith('http') or url.startswith('https'):
                resources_urls.append(url)
            elif url.startswith('//'):
                resources_urls.append('https:' + url)
            else:
                resources_urls.append(BASE_URL + url)

        # we match links to youtube videos as <a href> and add them to the
        # download list
        re_youtube_links = re.compile(r'&lt;a href=(?:&#34;|")(https?\:\/\/(?:www\.)?(?:youtube\.com|youtu\.?be)\/.*?)(?:&#34;|")')
        youtube_links = re_youtube_links.findall(text)
        resources_urls += youtube_links

        return resources_urls

    def extract_sections_from_html(self, page, BASE_URL):
        """
        Extract sections (Section->SubSection) from the html page
        """
        def _make_url(section_soup):  # FIXME: Extract from here and test
            try:
                return BASE_URL + section_soup.ul.a['href']
            except AttributeError:
                # Section might be empty and contain no links
                return None

        def _get_section_name(section_soup):  # FIXME: Extract from here and test
            try:
                return section_soup.h3.a.string.strip()
            except AttributeError:
                return None

        def _make_subsections(section_soup):
            try:
                subsections_soup = section_soup.ul.find_all("li")
            except AttributeError:
                return []
            # FIXME correct extraction of subsection.name (unicode)
            subsections = [SubSection(position=i,
                                      url=BASE_URL + s.a['href'],
                                      name=s.p.get_text().replace('current section',''))
                           for i, s in enumerate(subsections_soup, 1)]

            return subsections

        soup = BeautifulSoup(page)
        sections_soup = soup.find_all('div', attrs={'class': 'chapter'})

        sections = [Section(position=i,
                            name=_get_section_name(section_soup),
                            url=_make_url(section_soup),
                            subsections=_make_subsections(section_soup))
                    for i, section_soup in enumerate(sections_soup, 1)]
        # Filter out those sections for which name or url could not be parsed
        sections = [section for section in sections
                    if section.name and section.url]

        return sections

    def extract_courses_from_html(self, page, BASE_URL):
        """
        Extracts courses (Course) from the html page
        """
        soup = BeautifulSoup(page)

        # First, try with new course structure (as of December 2017).  If
        # that doesn't work, we fallback to an older course structure
        # (released with version 0.1.6). If even that doesn't work, then we
        # try with the oldest course structure (that was current before
        # version 0.1.6).
        #
        # rbrito---This code is ugly.

        courses_soup = soup.find_all('article', 'course')
        if len(courses_soup) == 0:
            courses_soup = soup.find_all('div', 'course')
        if len(courses_soup) == 0:
            courses_soup = soup.find_all('div', 'course audit')

        courses = []

        for course_soup in courses_soup:
            course_id = None
            course_name = course_soup.h3.text.strip()
            course_url = None
            course_state = 'Not yet'
            try:
                # started courses include the course link in the href attribute
                course_url = BASE_URL + course_soup.a['href']
                if course_url.endswith('info') or course_url.endswith('info/') or course_url.endswith('course') or course_url.endswith('course/'):
                    course_state = 'Started'
                # The id of a course in edX is composed by the path
                # {organization}/{course_number}/{course_run}
                course_id = course_soup.a['href'][9:-5]
            except KeyError:
                pass
            courses.append(Course(course_id=course_id,
                                  course_name=course_name,
                                  course_url=course_url,
                                  course_state=course_state))

        return courses


class CurrentEdXPageExtractor(ClassicEdXPageExtractor):
    """
    A new page extractor for the recent changes in layout of edx
    """
    def extract_unit(self, text, BASE_URL, file_formats):
        re_metadata = re.compile(r'data-metadata=&#39;(.*?)&#39;')
        videos = []
        match_metadatas = re_metadata.findall(text)
        for match_metadata in match_metadatas:
            metadata = html.unescape(match_metadata)
            metadata = json.loads(html.unescape(metadata))
            video_youtube_url = None
            re_video_speed = re.compile(r'1.0\d+\:(?:.*?)(.{11})')
            match_video_youtube_url = re_video_speed.search(metadata['streams'])
            if match_video_youtube_url is not None:
                video_id = match_video_youtube_url.group(1)
                video_youtube_url = 'https://youtube.com/watch?v=' + video_id
            # notice that the concrete languages come now in
            # so we can eventually build the full urls here
            # subtitles_download_urls = {sub_lang:
            #                            BASE_URL + metadata['transcriptTranslationUrl'].replace('__lang__', sub_lang)
            #                            for sub_lang in metadata['transcriptLanguages'].keys()}
            available_subs_url = BASE_URL + metadata['transcriptAvailableTranslationsUrl']
            sub_template_url = BASE_URL + metadata['transcriptTranslationUrl'].replace('__lang__', '%s')
            mp4_urls = [url for url in metadata['sources'] if url.endswith('.mp4')]
            videos.append(Video(video_youtube_url=video_youtube_url,
                                available_subs_url=available_subs_url,
                                sub_template_url=sub_template_url,
                                mp4_urls=mp4_urls))

        resources_urls = self.extract_resources_urls(text, BASE_URL,
                                                     file_formats)
        return Unit(videos=videos, resources_urls=resources_urls)

    def extract_sections_from_html(self, page, BASE_URL):
        """
        Extract sections (Section->SubSection) from the html page
        """
        def _make_url(section_soup):  # FIXME: Extract from here and test
            try:
                return BASE_URL + section_soup.div.div.a['href']
            except AttributeError:
                # Section might be empty and contain no links
                return None

        def _get_section_name(section_soup):  # FIXME: Extract from here and test
            try:
                return section_soup['aria-label'][:-8] # -8 cuts the submenu word
            except AttributeError:
                return None

        def _make_subsections(section_soup):
            try:
                subsections_soup = section_soup.find_all('div', attrs={'class': 'menu-item'})
            except AttributeError:
                return []
            # FIXME correct extraction of subsection.name (unicode)
            subsections = [SubSection(position=i,
                                      url=BASE_URL + s.a['href'],
                                      name=s.p.string)
                           for i, s in enumerate(subsections_soup, 1)]

            return subsections

        soup = BeautifulSoup(page)
        sections_soup = soup.find_all('div', attrs={'class': 'chapter-content-container'})

        sections = [Section(position=i,
                            name=_get_section_name(section_soup),
                            url=_make_url(section_soup),
                            subsections=_make_subsections(section_soup))
                    for i, section_soup in enumerate(sections_soup, 1)]
        # Filter out those sections for which name or url could not be parsed
        sections = [section for section in sections
                    if section.name and section.url]

        return sections


class NewEdXPageExtractor(CurrentEdXPageExtractor):
    """
    A new page extractor for the latest changes in layout of edx
    """

    def extract_sections_from_html(self, page, BASE_URL):
        """
        Extract sections (Section->SubSection) from the html page
        """
        def _make_url(section_soup):  # FIXME: Extract from here and test
            try:
                return section_soup.a['href']
            except AttributeError:
                # Section might be empty and contain no links
                return None

        def _get_section_name(section_soup):  # FIXME: Extract from here and test
            try:
                return section_soup.button.h3.string.strip()
            except AttributeError:
                return None

        def _make_subsections(section_soup):
            try:
                subsections_soup = section_soup.find_all('li', class_=['subsection'])
            except AttributeError:
                return []
            # FIXME correct extraction of subsection.name (unicode)
            subsections = [SubSection(position=i,
                                      url=s.a['href'],
                                      name=s.a.h4.string.strip())
                           for i, s in enumerate(subsections_soup, 1)]

            return subsections

        soup = BeautifulSoup(page)
        sections_soup = soup.find_all('li', class_=['outline-item','section'])

        sections = [Section(position=i,
                            name=_get_section_name(section_soup),
                            url=_make_url(section_soup),
                            subsections=_make_subsections(section_soup))
                    for i, section_soup in enumerate(sections_soup, 1)]
        # Filter out those sections for which name could not be parsed
        sections = [section for section in sections
                    if section.name]

        return sections


class RobustEdXPageExtractor(NewEdXPageExtractor):
    def extract_units_from_html(self, page, BASE_URL, file_formats, page_title):
        """
        Extract Units from the html of a subsection webpage as a list of
        resources
        """
        soup = BeautifulSoup(page)
        units_soup = soup.find_all('div', attrs={'class': 'vert'})

        units = []

        for unit_soup in units_soup:
            unit = self.extract_unit(unit_soup, BASE_URL, file_formats)
            if len(unit.videos) > 0 or len(unit.resources_urls) > 0:
                units.append(unit)

        # # If a unit is of these types, download it as a web page
        # content_types = ['discussion', 'html', 'poll', 'problem', 'survey']
        # block_type = re.findall(r'data-block-type="(.+?)"', page)
        # if [x for x in block_type if x in content_types]:
        #     units.append(WebpageUnit(page_title=page_title, content=page))
        new_page = self.absolute_path_page(page, BASE_URL)
        units.append(WebpageUnit(page_title=page_title, content=new_page))
        return units

    def extract_unit(self, unit_soup, BASE_URL, file_formats):
        videos = []
        resources_urls = []
        xblock_list = unit_soup.find_all('div', 'xblock')
        for xblock in xblock_list:
            xblock_type = xblock['data-block-type']
            if xblock_type == 'video':
                video_youtube_url = None
                available_subs_url = None
                sub_template_url = None
                mp4_urls = []
                video_download_button = xblock.find('a', 'btn-link video-sources video-download-button')
                if video_download_button:
                    mp4_urls.append(video_download_button['href'])
                subtitle_download_button = xblock.find('a', text=re.compile('^Download SubRip'))
                if subtitle_download_button:
                    available_subs_url = BASE_URL + subtitle_download_button['href']
                if not video_download_button and not subtitle_download_button:
                    re_metadata = re.compile(r'data-metadata=&#39;(.*?)&#39;')
                    match_metadatas = re_metadata.findall(str(unit_soup))
                    for match_metadata in match_metadatas:
                        metadata = html.unescape(match_metadata)
                        metadata = json.loads(html.unescape(metadata))
                        re_video_speed = re.compile(r'1.0\d+\:(?:.*?)(.{11})')
                        match_video_youtube_url = re_video_speed.search(metadata['streams'])
                        if match_video_youtube_url is not None:
                            video_id = match_video_youtube_url.group(1)
                            video_youtube_url = 'https://youtube.com/watch?v=' + video_id
                        available_subs_url = BASE_URL + metadata['transcriptAvailableTranslationsUrl']
                        sub_template_url = BASE_URL + metadata['transcriptTranslationUrl'].replace('__lang__', '%s')
                        mp4_urls = [url for url in metadata['sources'] if url.endswith('.mp4')]
                videos.append(Video(video_youtube_url=video_youtube_url,
                                    available_subs_url=available_subs_url,
                                    sub_template_url=sub_template_url,
                                    mp4_urls=mp4_urls))
            else:
                urls = self.extract_resources_urls(xblock, BASE_URL, file_formats)
                resources_urls.extend(urls)
        return Unit(videos=videos, resources_urls=resources_urls)


    def extract_resources_urls(self, soup, BASE_URL, file_formats):
        """
        Extract resources looking for <a> references in the webpage and
        matching the given file formats
        """
        formats = '|'.join(file_formats)
        re_resources_urls = re.compile(r'\<a href=(?:&#34;|")([^"&]*.(?:' + formats + '))(?:&#34;|")')
        resources_urls = []
        for url in re_resources_urls.findall(str(soup)):
            if url.startswith('http') or url.startswith('https'):
                resources_urls.append(url)
            elif url.startswith('//'):
                resources_urls.append('https:' + url)
            else:
                resources_urls.append(BASE_URL + url)

        # we match links to youtube videos as <a href> and add them to the download list
        re_youtube_links = re.compile(
            r'\<a href=(?:&#34;|")(https?\:\/\/(?:www\.)?(?:youtube\.com|youtu\.?be)\/.*?)(?:&#34;|")')
        youtube_links = re_youtube_links.findall(str(soup))
        resources_urls += youtube_links

        return resources_urls

    def absolute_path_page(self, page, base_url):
        """
        Replace the relative path of the image on the page with an absolute path
        return new page
        """
        soup = BeautifulSoup(page)
        image_elements = soup.find_all('img')
        for img_elem in image_elements:
            if img_elem['src'].startswith('/'):
                img_elem['src'] = base_url + img_elem['src']
        return str(soup)


def get_page_extractor(url):
    """
    factory method for page extractors
    """
    if (
        url.startswith('https://courses.edx.org') or
        url.startswith('https://mitxpro.mit.edu')
    ):
        return NewEdXPageExtractor()
    elif (
        url.startswith('https://edge.edx.org') or
        url.startswith('https://lagunita.stanford.edu') or
        url.startswith('https://www.fun-mooc.fr')
    ):
        return NewEdXPageExtractor()
    else:
        return ClassicEdXPageExtractor()


def is_youtube_url(url):
    re_youtube_url = re.compile(r'(https?\:\/\/(?:www\.)?(?:youtube\.com|youtu\.?be)\/.*?)')
    return re_youtube_url.match(url)
