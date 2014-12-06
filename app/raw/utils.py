"""
Some utilities for working with spiders
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from itertools import izip_longest
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
import magic
import subprocess
import pydocx
import os


HTML = 1
DOC = 2
DOCX = 3
PDF = 4


def list_spiders():
    settings = get_project_settings()
    crawler = Crawler(settings)
    return crawler.spiders.list()


def check_file_type(filepath, as_string=False):
    filetype = magic.from_file(filepath)
    if not filetype:
        # Filetype Could Not Be Determined
        return None
    elif filetype == 'empty':
        # Filetype Could Not Be Determined (file looks empty)
        return None
    elif filetype == 'very short file (no magic)':
        # Filetype Could Not Be Determined (very short file)
        return None
    elif "Microsoft Office Word" in filetype:
        return DOC if not as_string else 'DOC'
    elif filetype[0:4] == 'HTML':
        return HTML if not as_string else 'HTML'
    elif filetype == 'Microsoft Word 2007+':
        return DOCX if not as_string else 'DOCX'
    elif 'PDF' in filetype:
        return PDF if not as_string else 'PDF'
    else:
        # some other filetype that we don't account for
        return None


def doc_to_html(filepath, overwrite=False):
    """
    Converts a doc file to in-memory html string.

    :param filepath: full filepath to the file to convert
    :return: unicode string
    """
    html_file = '{}.html'.format(filepath)
    if not os.path.exists(html_file) or overwrite:
        cmd = ['abiword', '--to=html', '--to-name=fd://1', filepath]
        res = subprocess.check_output(cmd)
        with open(html_file, 'wb') as tmp:
            tmp.write(res)
    else:
        with open(html_file, 'rb') as tmp:
            res = tmp.read()
    return res.decode('utf-8')


def docx_to_html(filepath, overwrite=False):
    """
    Converts docx file to in-memory html string

    :param filepath: full path to the file to convert
    :return: unicode string
    """
    html_file = '{}.html'.format(filepath)
    if not os.path.exists(html_file) or overwrite:
        res = pydocx.docx2html(filepath)
        with open(html_file, 'wb') as tmp:
            tmp.write(res.encode('utf-8'))
    else:
        with open(html_file, 'rb') as tmp:
            res = tmp.read().decode('utf-8')
    return res


def get_file_path(rel_path):
    """
    Given a relative path for a file downloaded by scrapy, get the absolute path
    """
    files_folder = getattr(settings, 'SCRAPY_FILES_PATH', None)
    if files_folder is None:
        raise ImproperlyConfigured("No SCRAPY_FILES_PATH defined")

    file_path = os.path.join(files_folder, rel_path)
    if not os.path.exists(file_path):
        raise RuntimeError("Could not find file at {}".format(file_path))

    return file_path


def to_string(obj, encoding='utf-8'):
    """
    Converts unicode objects to strings, and returns strings directly
    """
    if isinstance(obj, basestring):
        if isinstance(obj, unicode):
            obj = obj.encode(encoding)
    return obj


def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)
