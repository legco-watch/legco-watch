"""
Some utilities for working with spiders
"""
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
import magic


def list_spiders():
    settings = get_project_settings()
    crawler = Crawler(settings)
    return crawler.spiders.list()


def check_file_type(filepath):
    filetype = magic.from_file(filepath)
    if not filetype:
        return 'Filetype Could Not Be Determined'
    elif filetype == 'empty':
        return 'Filetype Could Not Be Determined (file looks empty)'
    elif filetype == 'very short file (no magic)':
        return 'Filetype Could Not Be Determined (very short file)'
    elif "Microsoft Office Word" in filetype:
        return 'Microsoft Word Doc'
    else:
        return filetype