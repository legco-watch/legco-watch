"""
Some utilities for working with spiders
"""
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings


def list_spiders():
    settings = get_project_settings()
    crawler = Crawler(settings)
    return crawler.spiders.list()