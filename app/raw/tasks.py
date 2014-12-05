from __future__ import absolute_import
from datetime import datetime
import logging
from celery import shared_task
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
import os
from raw.models import ScrapeJob

from raw.scraper.spiders.legco_library import LibraryAgendaSpider
from raw.scraper.spiders.members import LibraryMemberSpider

logger = logging.getLogger('legcowatch')


def generate_scrape_name(spider_name):
    # Assume we don't need second resolution
    timestamp = datetime.now().strftime('%y%m%d%H%m')
    return '{}{}.jsonl'.format(spider_name, timestamp)


def complete_job(scrapejob_id):
    """
    creates a callback for updating a ScrapeJob once a scrape has completed
    """
    def cb():
        updated_count = ScrapeJob.objects.filter(id=scrapejob_id).update(completed=datetime.now())
        if updated_count != 1:
            logger.warn('Expected one job when completing ScrapeJob, found {} with id {}'.format(updated_count, scrapejob_id))
    return cb


def is_spider_scraping(spider_name):
    """
    Checks if a spider is already scraping.  This looks for ScrapeJobs that are not completed
    and which have been started in the last hour.
    :param spider_name: str name of the spider
    :return: False if no ScrapeJob is found, otherwise returns the ScrapeJob instance
    """
    try:
        pending_job = ScrapeJob.objects.pending_jobs().filter(spider=spider_name).latest('scheduled')
    except ScrapeJob.DoesNotExist as e:
        return False
    return pending_job


@shared_task
def scrape_task(spider_name):
    """
    Asynchronous task for individual scrapes that is executed by Celery workers.
    :param spider_name: str name of the spider that should be run
    :return: the full path of the jsonlines output file to which results are stored
    """
    # create and configure the spider
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    try:
        spider = crawler.spiders.create(spider_name)
    except KeyError as e:
        # No spider found.
        raise RuntimeError('Could not find spider with name {}'.format(spider_name))

    # Check to see if we're already running a scrape by looking for open ScrapeJobs
    is_scraping = is_spider_scraping(spider_name)
    if is_scraping is False:
        # configure the output
        output_name = generate_scrape_name(spider_name)
        output_path = os.path.join(settings.get('DATA_DIR_BASE'), 'scrapes', output_name)
        settings.overrides['FEED_URI'] = output_path

        # Create the ScrapeJob record
        job = ScrapeJob.objects.create(
            spider=spider_name,
            scheduled=datetime.now(),
            # see http://stackoverflow.com/questions/18872854/getting-task-id-inside-a-celery-task
            job_id=scrape_task.request.id,
            raw_response=output_path
        )
        # and set up the callback for updating it
        complete_cb = complete_job(job.id)

        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.signals.connect(complete_cb, signals=signals.spider_closed)
        log.start(loglevel=log.INFO, logstdout=True)
        crawler.crawl(spider)
        crawler.start()
        reactor.run()
    else:
        job = is_scraping

    return job.raw_response
