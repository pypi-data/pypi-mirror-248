#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main module for the edx-helper.
It corresponds to the cli interface
"""

import argparse
import getpass
import json
import logging
import os
import pickle
import re
import sys

from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from concurrent import futures

from six.moves.http_cookiejar import CookieJar
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import (
    urlopen,
    build_opener,
    install_opener,
    HTTPCookieProcessor,
    Request,
    urlretrieve,
)

import requests

from edx_helper import __version__

from .common import (
    YOUTUBE_DL_CMD,
    DEFAULT_CACHE_FILENAME,
    Unit,
    WebpageUnit,
    Video,
    ExitCode,
    DEFAULT_FILE_FORMATS,
)
from .parsing import (
    edx_json2srt,
    get_page_extractor,
    is_youtube_url,
    EdXJsonExtractor,
    RobustEdXPageExtractor,
)
from .utils import (
    clean_filename,
    directory_name,
    execute_command,
    get_page_contents,
    get_page_contents_as_json,
    mkdir_p,
    remove_duplicates,
    deprecated,
    TqdmUpTo,
)

OPENEDX_SITES = {
    'edx': {
        'url': 'https://courses.edx.org',
        'courseware-selector': ('nav', {'aria-label': 'Course Navigation'}),
    },
    'edge': {
        'url': 'https://edge.edx.org',
        'courseware-selector': ('nav', {'aria-label': 'Course Navigation'}),
    },
    'stanford': {
        'url': 'https://lagunita.stanford.edu',
        'courseware-selector': ('nav', {'aria-label': 'Course Navigation'}),
    },
    'usyd-sit': {
        'url': 'http://online.it.usyd.edu.au',
        'courseware-selector': ('nav', {'aria-label': 'Course Navigation'}),
    },
    'fun': {
        'url': 'https://www.fun-mooc.fr',
        'courseware-selector': ('section', {'aria-label': 'Menu du cours'}),
    },
    'gwu-seas': {
        'url': 'http://openedx.seas.gwu.edu',
        'courseware-selector': ('nav', {'aria-label': 'Course Navigation'}),
    },
    'gwu-open': {
        'url': 'http://mooc.online.gwu.edu',
        'courseware-selector': ('nav', {'aria-label': 'Course Navigation'}),
    },
    'mitxpro': {
        'url': 'https://mitxpro.mit.edu',
        'courseware-selector': ('nav', {'aria-label': 'Course Navigation'}),
    },
    'bits': {
        'url': 'http://any-learn.bits-pilani.ac.in',
        'courseware-selector': ('nav', {'aria-label': 'Course Navigation'}),
    }
}
BASE_URL = OPENEDX_SITES['edx']['url']
EDX_HOMEPAGE = BASE_URL + '/user_api/v1/account/login_session'
EDX_LEARN_BASE_URL = 'https://learning.edx.org/course'
LOGIN_API = BASE_URL + '/login_ajax'
DASHBOARD = BASE_URL + '/dashboard'
COURSE_LIST_API = BASE_URL + '/api/learner_home/init'
COURSE_OUTLINE_API = BASE_URL + '/api/course_home/outline'
COURSE_SEQUENCE_API = BASE_URL + '/api/courseware/sequence'
COURSE_XBLOCK_API = BASE_URL + '/xblock'
COURSEWARE_SEL = OPENEDX_SITES['edx']['courseware-selector']


def change_openedx_site(site_name):
    """
    Changes the openedx website for the given one via the key
    """
    global BASE_URL
    global EDX_LEARN_BASE_URL
    global EDX_HOMEPAGE
    global LOGIN_API
    global DASHBOARD
    global COURSEWARE_SEL

    sites = sorted(OPENEDX_SITES.keys())
    if site_name not in sites:
        logging.error("OpenEdX platform should be one of: %s", ', '.join(sites))
        sys.exit(ExitCode.UNKNOWN_PLATFORM)

    BASE_URL = OPENEDX_SITES[site_name]['url']
    EDX_HOMEPAGE = BASE_URL + '/user_api/v1/account/login_session'
    LOGIN_API = BASE_URL + '/login_ajax'
    DASHBOARD = BASE_URL + '/dashboard'
    COURSEWARE_SEL = OPENEDX_SITES[site_name]['courseware-selector']


def _display_courses(courses):
    """
    List the courses that the user has enrolled.
    """
    logging.info('You can access %d courses', len(courses))

    for i, course in enumerate(courses, 1):
        logging.info('%2d - %s [%s]', i, course.course_name, course.course_id)
        logging.info('     %s', course.course_url)


def get_courses_info(url, headers):
    """
    Extracts the courses information.
    """
    logging.info('Extracting courses from dashboard api: %s', url)

    json_extractor = EdXJsonExtractor()
    courses_json = get_page_contents_as_json(url, headers)
    courses = json_extractor.extract_courses(courses_json)

    logging.debug('Data extracted: %s', courses)

    return courses


def _get_initial_token(url):
    """
    Create initial connection to get authentication token for future
    requests.

    Returns a string to be used in subsequent connections with the
    X-CSRFToken header or the empty string if we didn't find any token in
    the cookies.
    """
    logging.info('Getting initial CSRF token.')

    cookiejar = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cookiejar))
    install_opener(opener)
    opener.open(url)

    for cookie in cookiejar:
        if cookie.name == 'csrftoken':
            logging.info('Found CSRF token.')
            return cookie.value

    logging.warning('Did not find the CSRF token.')
    return ''


def get_available_sections(url, headers):
    """
    Extracts the sections and subsections from a given url
    """
    logging.debug("Extracting sections for :" + url)

    page = get_page_contents(url, headers)
    page_extractor = get_page_extractor(url)
    sections = page_extractor.extract_sections_from_html(page, BASE_URL)

    logging.debug("Extracted sections: " + str(sections))
    return sections


def get_available_sequential_blocks(course_id, headers):
    """
    Extracts the chapter blocks and sequential blocks for a given course id
    """

    url = COURSE_OUTLINE_API + '/' + course_id
    logging.info("Extracting chapter blocks and sequential blocks from: \n%s", url)

    resp_dict = get_page_contents_as_json(url, headers=headers)
    extractor = EdXJsonExtractor()
    blocks = extractor.extract_sequential_blocks(resp_dict)
    return blocks


def edx_get_subtitle(url, headers,
                     get_html=get_page_contents,
                     get_json=get_page_contents_as_json):
    """
    Return a string with the subtitles content from the url or None if no
    subtitles are available.
    """
    try:
        if ';' in url:  # non-JSON format (e.g. Stanford)
            return get_html(url, headers)
        else:
            json_object = get_json(url, headers)
            return edx_json2srt(json_object)
    except URLError as exception:
        logging.warning('edX subtitles (error: %s)', exception)
        return None
    except ValueError as exception:
        logging.warning('edX subtitles (error: %s)', exception)
        return None


def edx_login(url, headers, username, password):
    """
    Log in user into the openedx website.
    """
    logging.info('Logging into Open edX site: %s', url)

    post_data = urlencode({'email': username,
                           'password': password,
                           'remember': False}).encode('utf-8')

    request = Request(url, post_data, headers)
    try:
        response = urlopen(request)
    except HTTPError as e:
        logging.info('Error, cannot login: %s', e)
        return {'success': False}

    resp = json.loads(response.read().decode('utf-8'))

    return resp


def parse_args():
    """
    Parse the arguments/options passed to the program on the command line.
    """
    parser = argparse.ArgumentParser(prog='edx-helper',
                                     description='Get videos from the OpenEdX platform',
                                     epilog='For further use information,'
                                            'see the file README.md', )
    # positional
    parser.add_argument('course_urls',
                        nargs='*',
                        action='store',
                        default=[],
                        help='target course urls '
                             '(e.g., https://courses.edx.org/courses/BerkeleyX/CS191x/2013_Spring/info)')

    # optional
    parser.add_argument('-u',
                        '--username',
                        required=True,
                        action='store',
                        help='your edX username (email)')

    parser.add_argument('-p',
                        '--password',
                        action='store',
                        help='your edX password, '
                             'beware: it might be visible to other users on your system')

    parser.add_argument('-f',
                        '--format',
                        dest='format',
                        action='store',
                        default=None,
                        help='format of videos to download')

    parser.add_argument('-s',
                        '--with-subtitles',
                        dest='subtitles',
                        action='store_true',
                        default=False,
                        help='download subtitles with the videos')

    parser.add_argument('-o',
                        '--output-dir',
                        action='store',
                        dest='output_dir',
                        help='store the files to the specified directory',
                        default='Downloaded')

    parser.add_argument('-i',
                        '--ignore-errors',
                        dest='ignore_errors',
                        action='store_true',
                        default=False,
                        help='continue on download errors, to avoid stopping large downloads')

    sites = sorted(OPENEDX_SITES.keys())
    parser.add_argument('-x',
                        '--platform',
                        action='store',
                        dest='platform',
                        help='OpenEdX platform, one of: %s' % ', '.join(sites),
                        default='edx')

    parser.add_argument('--list-courses',
                        dest='list_courses',
                        action='store_true',
                        default=False,
                        help='list available courses')

    parser.add_argument('--filter-section',
                        dest='filter_section',
                        action='store',
                        default=None,
                        help='filters sections to be downloaded')

    parser.add_argument('--list-sections',
                        dest='list_sections',
                        action='store_true',
                        default=False,
                        help='list available sections')

    parser.add_argument('--youtube-dl-options',
                        dest='youtube_dl_options',
                        action='store',
                        default='',
                        help='set extra options to pass to youtube-dl')

    parser.add_argument('--prefer-cdn-videos',
                        dest='prefer_cdn_videos',
                        action='store_true',
                        default=False,
                        help='prefer CDN video downloads over youtube (BETA)')

    parser.add_argument('--export-filename',
                        dest='export_filename',
                        default=None,
                        help='filename where to put an exported list of urls. '
                             'Use dash "-" to output to stdout. '
                             'Download will not be performed if this option is '
                             'present')

    parser.add_argument('--export-format',
                        dest='export_format',
                        default='%(url)s',
                        help='export format string. Old-style python formatting '
                             'is used. Available variables: %%(url)s. Default: '
                             '"%%(url)s"')

    parser.add_argument('--list-file-formats',
                        dest='list_file_formats',
                        action='store_true',
                        default=False,
                        help='list the default file formats extracted')

    parser.add_argument('--file-formats',
                        dest='file_formats',
                        action='store',
                        default=None,
                        help='appends file formats to be extracted (comma '
                             'separated)')

    parser.add_argument('--overwrite-file-formats',
                        dest='overwrite_file_formats',
                        action='store_true',
                        default=False,
                        help='if active overwrites the file formats to be '
                             'extracted')

    parser.add_argument('--cache',
                        dest='cache',
                        action='store_true',
                        default=False,
                        help='create and use a cache of extracted resources')

    parser.add_argument('--dry-run',
                        dest='dry_run',
                        action='store_true',
                        default=False,
                        help='makes a dry run, only lists the resources')

    parser.add_argument('--sequential',
                        dest='sequential',
                        action='store_true',
                        default=False,
                        help='extracts the resources from the pages sequentially')

    parser.add_argument('--quiet',
                        dest='quiet',
                        action='store_true',
                        default=False,
                        help='omit as many messages as possible, only printing errors')

    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        default=False,
                        help='print lots of debug information')

    parser.add_argument('--version',
                        action='version',
                        version=__version__,
                        help='display version and exit')

    args = parser.parse_args()

    # Initialize the logging system first so that other functions
    # can use it right away.
    if args.debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(name)s[%(funcName)s] %(message)s')
    elif args.quiet:
        logging.basicConfig(level=logging.ERROR,
                            format='%(name)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(message)s')

    return args


def edx_get_headers():
    """
    Build the Open edX headers to create future requests.
    """
    logging.info('Building initial headers for future requests.')

    headers = {
        'User-Agent': 'edX-downloader/0.01',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': EDX_HOMEPAGE,
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': _get_initial_token(EDX_HOMEPAGE),
    }

    logging.debug('Headers built: %s', headers)
    return headers


@deprecated
def extract_units(url, headers, file_formats):
    """
    Parses a webpage and extracts its resources e.g. video_url, sub_url, etc.
    """
    logging.info("Processing '%s'", url)

    page = get_page_contents(url, headers)
    page_extractor = get_page_extractor(url)
    units = page_extractor.extract_units_from_html(page, BASE_URL, file_formats)

    return units


def extract_units_from_vertical_block(vertical_block, headers, file_formats):
    """
    Parses a webpage and extracts its resources e.g. video_url, sub_url, etc.
    """
    params = {
        'exam_access': '',
        'show_title': 1,
        'show_bookmark': 0,
        'recheck_access': 1,
        'view': 'student_view'
    }
    vertical_block_api = COURSE_XBLOCK_API + '/' + vertical_block.block_id + '?%s' % urlencode(params)
    logging.debug("Extracting units from: \n'%s'", vertical_block_api)

    page_title = vertical_block.name
    page = get_page_contents(vertical_block_api, headers)
    page_extractor = RobustEdXPageExtractor()
    units = page_extractor.extract_units_from_html(page, BASE_URL, file_formats, page_title)
    return units


def extract_units_from_sequential_block(block, headers, file_formats):
    """
    Parses a webpage and extracts its resources e.g. video_url, sub_url, etc.
    """
    logging.info("Processing '%s'", block.url)

    url = COURSE_SEQUENCE_API + '/' + block.block_id
    logging.debug("Extracting units from: \n%s" + url)

    json_extractor = EdXJsonExtractor()
    resp_dict = get_page_contents_as_json(url, headers)
    vertical_blocks = json_extractor.extract_vertical_blocks(resp_dict, EDX_LEARN_BASE_URL)
    all_units = []
    for block in vertical_blocks:
        units = extract_units_from_vertical_block(block, headers, file_formats)
        all_units.extend(units)
    return all_units


@deprecated
def extract_all_units_in_sequence(urls, headers, file_formats):
    """
    Returns a dict of all the units in the selected_sections: {url, units}
    sequentially, this is clearer for debug purposes
    """
    logging.info('Extracting all units information in sequentially.')
    logging.debug('urls: ' + str(urls))

    units = [extract_units(url, headers, file_formats) for url in urls]
    all_units = dict(zip(urls, units))

    return all_units


def extract_units_in_sequence(sequential_block_list, headers, file_formats):
    """
    Returns a dict of all the units in the selected_sections: {section, units}
    sequentially, this is clearer for debug purposes
    """
    logging.info('Extracting all units information in sequentially.')
    units = [extract_units_from_sequential_block(block, headers, file_formats) for block in sequential_block_list]
    all_units = dict(zip(sequential_block_list, units))
    return all_units


@deprecated
def extract_all_units_in_parallel(urls, headers, file_formats):
    """
    Returns a dict of all the units in the selected_sections: {url, units}
    in parallel
    """
    logging.info('Extracting all units information in parallel.')
    logging.debug('urls: ' + str(urls))

    mapfunc = partial(extract_units, file_formats=file_formats, headers=headers)
    pool = ThreadPool(16)
    units = pool.map(mapfunc, urls)
    pool.close()
    pool.join()
    all_units = dict(zip(urls, units))

    return all_units


def extract_units_in_parallel(sequential_block_list, headers, file_formats):
    """
    Returns a dict of all the units in the selected_sections: {url, units}
    in parallel
    """
    logging.info('Extracting all units information in parallel.')

    mapfunc = partial(extract_units_from_sequential_block, file_formats=file_formats, headers=headers)
    pool = ThreadPool(16)
    units = pool.map(mapfunc, sequential_block_list)
    pool.close()
    pool.join()
    all_units = dict(zip(sequential_block_list, units))

    return all_units


def _display_sections_menu(course, sections):
    """
    List the weeks for the given course.
    """
    num_sections = len(sections)

    logging.info('%s [%s] has %d sections so far', course.course_name, course.course_id, num_sections)
    for i, section in enumerate(sections, 1):
        logging.info('%2d - Download %s videos', i, section.name)


def _filter_sections(index, sections):
    """
    Get the sections for the given index.

    If the index is not valid (that is, None, a non-integer, a negative
    integer, or an integer above the number of the sections), we choose all
    sections.
    """
    num_sections = len(sections)

    logging.info('Filtering sections')

    if index is not None:
        try:
            index = int(index)
            if 0 < index <= num_sections:
                logging.info('Sections filtered to: %d', index)
                return [sections[index - 1]]
            else:
                pass  # log some info here
        except ValueError:
            pass  # log some info here
    else:
        pass  # log some info here

    return sections


def _display_sections(sections):
    """
    Displays a tree of section(s) and subsections
    """
    logging.info('Downloading %d section(s)', len(sections))

    for section in sections:
        logging.info('Section %2d: %s', section.position, section.name)
        for subsection in section.subsections:
            logging.info('  %s', subsection.name)


def _display_blocks(blocks):
    """
    Displays a tree of blocks
    """
    logging.info('Downloading %d block(s)', len(blocks))

    for block in blocks:
        logging.info('block %2d: %s', block.position, block.name)
        for sub_block in block.children:
            logging.info('  %s', sub_block.name)


def parse_courses(args, available_courses):
    """
    Parses courses options and returns the selected_courses.
    """
    if args.list_courses:
        _display_courses(available_courses)
        exit(ExitCode.OK)

    if len(args.course_urls) == 0:
        logging.error('You must pass the URL of at least one course, check the correct url with --list-courses')
        exit(ExitCode.MISSING_COURSE_URL)

    selected_courses = [available_course
                        for available_course in available_courses
                        for url in args.course_urls
                        if available_course.course_url == url]
    if len(selected_courses) == 0:
        logging.error('You have not passed a valid course url, check the correct url with --list-courses')
        exit(ExitCode.INVALID_COURSE_URL)
    return selected_courses


def parse_sections(args, selections):
    """
    Parses sections options and returns selections filtered by
    selected_sections
    """
    if args.list_sections:
        for selected_course, selected_sections in selections.items():
            _display_sections_menu(selected_course, selected_sections)
        exit(ExitCode.OK)

    if not args.filter_section:
        return selections

    filtered_selections = {selected_course: _filter_sections(args.filter_section, selected_sections)
                           for selected_course, selected_sections in selections.items()}
    return filtered_selections


def parse_file_formats(args):
    """
    parse options for file formats and builds the array to be used
    """
    file_formats = DEFAULT_FILE_FORMATS

    if args.list_file_formats:
        logging.info(file_formats)
        exit(ExitCode.OK)

    if args.overwrite_file_formats:
        file_formats = []

    if args.file_formats:
        new_file_formats = args.file_formats.split(",")
        file_formats.extend(new_file_formats)

    logging.debug("file_formats: %s", file_formats)
    return file_formats


def _display_selections(selections):
    """
    Displays the course, sections and subsections to be downloaded
    """
    for selected_course, selected_sections in selections.items():
        logging.info('Downloading %s [%s]',
                     selected_course.course_name, selected_course.course_id)
        _display_sections(selected_sections)


def _display_selection_blocks(selections):
    """
    Displays the course, chapter blocks and sequential blocks to be downloaded
    """
    for selected_course, selected_blocks in selections.items():
        logging.info('Downloading %s [%s]',
                     selected_course.course_name, selected_course.course_id)
        _display_blocks(selected_blocks)


def parse_units(all_units):
    """
    Parses units options and corner cases
    """
    flat_units = [unit for units in all_units.values() for unit in units]
    if len(flat_units) < 1:
        logging.warning('No downloadable video found.')
        exit(ExitCode.NO_DOWNLOADABLE_VIDEO)


def _subtitles_info(video, target_dir):
    """
    Builds a dict {url: filename} for the subtitles, based on the
    filename_prefix of the video
    """
    downloads = {}
    if video.available_subs_url:
        url = video.available_subs_url
        filename = url.slit('/')[-1] if url.endswith('.srt') else None
        if not filename or not os.path.exists(os.path.join(target_dir, filename)):
            downloads[url] = filename
    if video.sub_template_url:
        url = video.sub_template_url
        filename = url.slit('/')[-1] if url.endswith('.srt') else None
        if not filename or not os.path.exists(os.path.join(target_dir, filename)):
            downloads[url] = filename
    return downloads


def _build_url_downloads(urls, target_dir, filename_prefix):
    """
    Builds a dict {url: filename} for the given urls
    If it is a youtube url it uses the valid template for youtube-dl
    otherwise just takes the name of the file from the url
    """
    downloads = {url: _build_filename_from_url(url, target_dir, filename_prefix) for url in urls}
    return downloads


def _build_filename_from_url(url, target_dir, filename_prefix):
    """
    Builds the appropriate filename for the given args
    """
    if is_youtube_url(url):
        filename_template = filename_prefix + "-%(title)s-%(id)s.%(ext)s"
        filename = os.path.join(target_dir, filename_template)
    else:
        original_filename = url.rsplit('/', 1)[1]
        filename = os.path.join(target_dir,
                                filename_prefix + '-' + original_filename)

    return filename


def download_url(url, filename, headers, args):
    """
    Downloads the given url in filename.
    """

    if is_youtube_url(url) and args.prefer_cdn_videos:
        pass
    elif is_youtube_url(url):
        download_youtube_url(url, filename, args)
    else:
        import requests
        from tqdm.auto import tqdm
        # FIXME: Ugly hack for coping with broken SSL sites:
        # https://www.cs.duke.edu/~angl/papers/imc10-cloudcmp.pdf
        #
        # We should really ask the user if they want to stop the downloads
        # or if they are OK proceeding without verification.
        #
        # Note that skipping verification by default could be a problem for
        # people's lives if they happen to live ditatorial countries.
        #
        # Note: The mess with various exceptions being caught (and their
        # order) is due to different behaviors in different Python versions
        # (e.g., 2.7 vs. 3.4).
        try:
            # mitxpro fix for downloading compressed files
            if 'zip' in url and 'mitxpro' in url:
                urlretrieve(url, filename)
                desc = url.split('/')[-1]
                with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=desc) as t:
                    urlretrieve(url, filename, reporthook=t.update_to, data=None)
                    t.total = t.n
            else:
                response = requests.get(url, headers=headers, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                desc = url.split('/')[-1]
                with open(filename, 'wb') as fd:
                    with tqdm.wrapattr(fd, "write", miniters=1, total=total_size, desc=desc) as fdw:
                        for chunk in response.iter_content(chunk_size=4096):
                            fdw.write(chunk)
        except Exception as e:
            logging.warning('Got SSL/Connection error: %s', e)
            if not args.ignore_errors:
                logging.warning('Hint: if you want to ignore this error, add '
                                '--ignore-errors option to the command line')
                raise e
            else:
                logging.warning('SSL/Connection error ignored: %s', e)


def download_youtube_url(url, filename, args):
    """
    Downloads a youtube URL and applies the filters from args
    """
    logging.info('Downloading video with URL %s from YouTube.', url)
    video_format_option = args.format + '/mp4' if args.format else 'mp4'
    cmd = YOUTUBE_DL_CMD + ['-o', filename, '-f', video_format_option]

    if args.subtitles:
        cmd.append('--all-subs')
    cmd.extend(args.youtube_dl_options.split())
    cmd.append(url)

    execute_command(cmd, args)


def download_subtitle(url, filename, headers):
    """
    Downloads the subtitle from the url and transforms it to the srt format
    """
    subs_string = edx_get_subtitle(url, headers)
    if subs_string:
        full_filename = os.path.join(os.getcwd(), filename)
        with open(full_filename, 'wb+') as f:
            f.write(subs_string.encode('utf-8'))


def download_subtitle_without_name(url, target_dir, filename, headers):
    """
    Downloads the subtitle from the url
    """
    # response = requests.get(url, headers)
    response = requests.get(url)
    if not filename:
        resp_headers = response.headers['Content-Disposition']
        m = re.compile(r'filename="(.*)"').search(resp_headers)
        if m:
            filename = m.group(1)
        else:
            logging.error('Not setting file name for: %s', url)
            return
    file_path = os.path.join(target_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(response.content)


def skip_or_download(downloads, headers, args, f=download_url):
    """
    downloads url into filename using download function f,
    if filename exists it skips
    """
    for url, filename in downloads.items():
        if os.path.exists(filename):
            logging.info('[skipping] %s => %s', url, filename)
            continue
        else:
            logging.info('[download] %s => %s', url, filename)
        if args.dry_run:
            continue
        f(url, filename, headers, args)


def skip_or_save(file_path, content):
    """
    save content into file  if it not exists
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)


def download_video(video, args, target_dir, filename_prefix, headers):
    if args.prefer_cdn_videos or video.video_youtube_url is None:
        mp4_downloads = _build_url_downloads(video.mp4_urls, target_dir,
                                             filename_prefix)
        skip_or_download(mp4_downloads, headers, args)
    else:
        if video.video_youtube_url is not None:
            youtube_downloads = _build_url_downloads([video.video_youtube_url],
                                                     target_dir,
                                                     filename_prefix)
            skip_or_download(youtube_downloads, headers, args)

    # the behavior with subtitles is different, since the subtitles don't know
    # the destination name until the video is downloaded with youtube-dl
    # also, subtitles must be transformed from the raw data to the srt format
    if args.subtitles:
        sub_downloads = _subtitles_info(video, target_dir)
        logging.info(sub_downloads)
        for url, filename in sub_downloads.items():
            download_subtitle_without_name(url, target_dir, filename, headers)


def download_unit(unit, args, target_dir, filename_prefix, headers):
    """
    Downloads the urls in unit based on args in the given target_dir
    with filename_prefix
    """
    if len(unit.videos) == 1:
        download_video(unit.videos[0], args, target_dir, filename_prefix,
                       headers)
    else:
        # we change the filename_prefix to avoid conflicts when downloading
        # subtitles
        for i, video in enumerate(unit.videos, 1):
            new_prefix = filename_prefix + ('-%02d' % i)
            download_video(video, args, target_dir, new_prefix, headers)

    res_downloads = _build_url_downloads(unit.resources_urls, target_dir,
                                         filename_prefix)
    skip_or_download(res_downloads, headers, args)
    if isinstance(unit, WebpageUnit):
        file_name = filename_prefix + '-' + clean_filename(unit.page_title) + '.html'
        file_path = os.path.join(target_dir, file_name)
        skip_or_save(file_path, unit.content)


def download(args, selections, all_units, headers):
    """
    Downloads all the resources based on the selections
    """
    logging.info("Output directory: " + args.output_dir)

    executor = futures.ThreadPoolExecutor()
    for selected_course, selected_blocks in selections.items():
        course_name = directory_name(selected_course.course_name)
        for selected_block in selected_blocks:
            section_dir = "%02d-%s" % (selected_block.position, selected_block.name)
            section_path = os.path.join(args.output_dir, course_name, clean_filename(section_dir))
            mkdir_p(section_path)
            for sequential_block in selected_block.children:
                seq_dir = "%02d-%s" % (sequential_block.position, sequential_block.name)
                seq_path = os.path.join(args.output_dir, course_name,
                                        clean_filename(section_dir), clean_filename(seq_dir))
                mkdir_p(seq_path)
                counter = 0
                units = all_units.get(sequential_block, [])
                for unit in units:
                    counter += 1
                    filename_prefix = "%02d" % counter
                    if args.sequential:
                        download_unit(unit, args, seq_path, filename_prefix, headers)
                    else:
                        executor.submit(download_unit, unit, args, seq_path, filename_prefix, headers)
    executor.shutdown(wait=True)


def remove_repeated_urls(all_units):
    """
    Removes repeated urls from the units, it does not consider subtitles.
    This is done to avoid repeated downloads.
    """
    existing_urls = set()
    filtered_units = {}
    for url, units in all_units.items():
        reduced_units = []
        for unit in units:
            videos = []
            for video in unit.videos:
                # we don't analyze the subtitles for repetition since
                # their size is negligible for the goal of this function
                video_youtube_url = None
                if video.video_youtube_url not in existing_urls:
                    video_youtube_url = video.video_youtube_url
                    existing_urls.add(video_youtube_url)

                mp4_urls, existing_urls = remove_duplicates(video.mp4_urls, existing_urls)

                if video_youtube_url is not None or len(mp4_urls) > 0:
                    videos.append(Video(video_youtube_url=video_youtube_url,
                                        available_subs_url=video.available_subs_url,
                                        sub_template_url=video.sub_template_url,
                                        mp4_urls=mp4_urls))

            resources_urls, existing_urls = remove_duplicates(unit.resources_urls, existing_urls)

            if len(videos) > 0 or len(resources_urls) > 0:
                reduced_units.append(Unit(videos=videos,
                                          resources_urls=resources_urls))

        filtered_units[url] = reduced_units
    return filtered_units


def num_urls_in_units_dict(units_dict):
    """
    Counts the number of urls in a all_units dict, it ignores subtitles from
    its counting.
    """
    num_urls = 0

    for units in units_dict.values():
        for unit in units:
            for video in unit.videos:
                num_urls += int(video.video_youtube_url is not None)
                num_urls += int(video.available_subs_url is not None)
                num_urls += int(video.sub_template_url is not None)
                num_urls += len(video.mp4_urls)
            num_urls += len(unit.resources_urls)

    return num_urls


def extract_all_units_with_cache(all_urls, headers, file_formats,
                                 filename=DEFAULT_CACHE_FILENAME,
                                 extractor=extract_all_units_in_parallel):
    """
    Extracts the units which are not in the cache and extract their resources
    returns the full list of units (cached+new)

    The cache is used to improve speed because it avoids requesting already
    known (and extracted) objects from URLs. This is useful to follow courses
    week by week since we won't parse the already known subsections/units,
    additionally it speeds development of code unrelated to extraction.
    """
    cached_units = {}

    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            cached_units = pickle.load(f)

    # we filter the cached urls
    new_urls = [url for url in all_urls if url not in cached_units]
    logging.info('loading %d urls from cache [%s]', len(cached_units.keys()),
                 filename)
    new_units = extractor(new_urls, headers, file_formats)
    all_units = cached_units.copy()
    all_units.update(new_units)

    return all_units


def extract_units_with_cache(sequential_block_list, headers, file_formats,
                             filename=DEFAULT_CACHE_FILENAME,
                             extractor=extract_units_in_parallel):
    """
    Extracts the units which are not in the cache and extract their resources
    returns the full list of units (cached+new)
    """
    cached_units = {}

    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            cached_units = pickle.load(f)

    # we filter the cached urls
    missing_sequential_blocks = [sequential_block
                                 for sequential_block in sequential_block_list
                                 if sequential_block not in cached_units]
    logging.info('loading %d urls from cache [%s]', len(cached_units.keys()),
                 filename)
    new_units = extractor(missing_sequential_blocks, headers, file_formats)
    all_units = cached_units.copy()
    all_units.update(new_units)

    return all_units


def write_units_to_cache(units, filename=DEFAULT_CACHE_FILENAME):
    """
    writes units to cache
    """
    logging.info('writing %d urls to cache [%s]', len(units.keys()),
                 filename)
    with open(filename, 'wb') as f:
        pickle.dump(units, f)


def extract_urls_from_units(all_units, format_):
    """
    Extract urls from units into a set of strings. Format is specified by
    the user. The original purpose of this function is to export urls into
    a file for external downloader.
    """
    all_urls = set()

    # Collect all urls into a set to remove duplicates
    for units in all_units.values():
        for unit in units:
            if isinstance(unit, Unit):
                for video in unit.videos:
                    if isinstance(video, Video):
                        for url in video.mp4_urls:
                            all_urls.add('%s\n' % (format_ % {'url': url}))
                    else:
                        raise TypeError('Unknown unit video type (%s) occured '
                                        'while exporting urls' % type(video))
                for url in unit.resources_urls:
                    all_urls.add('%s\n' % (format_ % {'url': url}))
            else:
                raise TypeError('Unknown unit type (%s) occured while '
                                'exporting urls' % type(unit))
    return list(all_urls)


def save_urls_to_file(urls, filename):
    """
    Save urls to file. Filename is specified by the user. The original
    purpose of this function is to export urls into a file for external
    downloader.
    """
    file_ = sys.stdout if filename == '-' else open(filename, 'w')
    file_.writelines(urls)
    file_.close()


def main():
    """
    Main program function
    """
    args = parse_args()
    logging.info('edx_helper version %s', __version__)
    file_formats = parse_file_formats(args)

    change_openedx_site(args.platform)

    # Query password, if not already passed by command line.
    if not args.password:
        args.password = getpass.getpass(stream=sys.stderr)

    if not args.username or not args.password:
        logging.error("You must supply username and password to log-in")
        exit(ExitCode.MISSING_CREDENTIALS)

    # Prepare Headers
    headers = edx_get_headers()

    # Login
    resp = edx_login(LOGIN_API, headers, args.username, args.password)
    if not resp.get('success', False):
        logging.error(resp.get('value', "Wrong Email or Password."))
        exit(ExitCode.WRONG_EMAIL_OR_PASSWORD)

    # Parse and select the available courses
    courses = get_courses_info(COURSE_LIST_API, headers)
    available_courses = [course for course in courses if course.course_state == 'Started']
    selected_courses = parse_courses(args, available_courses)

    # Parse the sections and build the selections dict filtered by sections
    if args.platform == 'edx':
        all_chapter_blocks = {selected_course: get_available_sequential_blocks(selected_course.course_id, headers)
                              for selected_course in selected_courses}
    else:
        all_chapter_blocks = {
            selected_course: get_available_sections(selected_course.course_url.replace('info', 'courseware'), headers)
            for selected_course in selected_courses}

    # selections = all_chapter_blocks
    selections = parse_sections(args, all_chapter_blocks)
    _display_selection_blocks(selections)

    # Extract the unit information (downloadable resources)
    # This parses the HTML of all the subsection.url and extracts
    # the URLs of the resources as Units.
    sequential_block_list = [sequential_block
                             for chapter_blocks_each_course in selections.values()
                             for chapter_block in chapter_blocks_each_course
                             for sequential_block in chapter_block.children]

    extractor = extract_units_in_parallel
    if args.sequential:
        extractor = extract_units_in_sequence

    if args.cache:
        all_units = extract_units_with_cache(sequential_block_list,
                                             headers, file_formats,
                                             extractor=extract_units_in_parallel)
    else:
        all_units = extractor(sequential_block_list, headers, file_formats)

    parse_units(all_units)

    if args.cache:
        write_units_to_cache(all_units)

    # This removes all repeated important urls
    # FIXME: This is not the best way to do it but it is the simplest, a
    # better approach will be to create symbolic or hard links for the repeated
    # units to avoid losing information
    # filtered_units = remove_repeated_urls(all_units)
    # num_all_urls = num_urls_in_units_dict(all_units)
    # num_filtered_urls = num_urls_in_units_dict(filtered_units)
    # logging.warning('Removed %d duplicated urls from %d in total',
    #              (num_all_urls - num_filtered_urls), num_all_urls)

    # finally we download or export all the resources
    if args.export_filename is not None:
        logging.info('exporting urls to file %s', args.export_filename)
        urls = extract_urls_from_units(all_units, args.export_format)
        save_urls_to_file(urls, args.export_filename)
    else:
        download(args, selections, all_units, headers)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("\n\nCTRL-C detected, shutting down....")
        sys.exit(ExitCode.OK)
