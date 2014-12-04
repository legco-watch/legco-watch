from __future__ import absolute_import
from celery import shared_task
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
import os

from raw.scraper.spiders.legco_library import LibraryAgendaSpider
from raw.scraper.spiders.members import LibraryMemberSpider

@shared_task
def run_scraper():
    output_name = 'foo.jl'
    spider = LibraryAgendaSpider()
    settings = get_project_settings()
    url_path = os.path.join(settings.get('DATA_DIR_BASE'), 'scrapes', output_name)
    settings.overrides['FEED_URI'] = url_path

    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start(loglevel=log.INFO, logstdout=True)
    reactor.run()
    return output_name
