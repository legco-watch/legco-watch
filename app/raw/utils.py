"""
Some utilities for working with spiders
"""
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
