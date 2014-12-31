from __future__ import absolute_import
from datetime import datetime, timedelta
import logging
from celery import shared_task
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
import os
from raw import processors
from raw.models import ScrapeJob
from django.conf import settings
from django.db.backends import BaseDatabaseWrapper
from django.db.backends.util import CursorWrapper

logger = logging.getLogger('legcowatch')


def generate_scrape_name(spider_name):
    # Assume we don't need second resolution
    timestamp = datetime.now().strftime('%y%m%d%H%M')
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
        cutoff = datetime.now() - timedelta(hours=1)
        pending_job = ScrapeJob.objects.pending_jobs()\
            .filter(spider=spider_name).filter(scheduled__gt=cutoff)\
            .latest('scheduled')
    except ScrapeJob.DoesNotExist as e:
        return False
    return pending_job


@shared_task
def do_scrape(spider_name):
    """
    Asynchronous task for individual scrapes that is executed by Celery workers.
    :param spider_name: str name of the spider that should be run
    :return: the full path of the jsonlines output file to which results are stored
    """
    # create and configure the spider
    crawl_settings = get_project_settings()
    # configure the output
    # Technically don't need this unless we actually do the scrape, but need to put
    # up here before the crawler is instantiated so the FEED_URI override is active
    output_name = generate_scrape_name(spider_name)
    output_path = os.path.join(crawl_settings.get('DATA_DIR_BASE'), 'scrapes', output_name)
    crawl_settings.overrides['FEED_URI'] = output_path
    crawler = Crawler(crawl_settings)
    crawler.configure()
    try:
        spider = crawler.spiders.create(spider_name)
    except KeyError as e:
        # No spider found.
        raise RuntimeError('Could not find spider with name {}'.format(spider_name))

    # Check to see if we're already running a scrape by looking for open ScrapeJobs
    is_scraping = is_spider_scraping(spider_name)
    if is_scraping is False:
        logger.info('Starting new scrape of {}'.format(spider_name))
        # Create the ScrapeJob record
        job_id = do_scrape.request.id
        if job_id is None:
            # Case if called directly without using Celery, put in a dummy job id
            timestamp = datetime.now().strftime('%y%m%d%H%M')
            job_id = 'MANUAL_RUN{}'.format(timestamp)
        job = ScrapeJob.objects.create(
            spider=spider_name,
            scheduled=datetime.now(),
            # see http://stackoverflow.com/questions/18872854/getting-task-id-inside-a-celery-task
            job_id=job_id,
            raw_response=output_path
        )
        # and set up the callback for updating it
        complete_cb = complete_job(job.id)

        # Connect the signals and logging, then start it up
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.signals.connect(complete_cb, signal=signals.spider_closed)
        log.start(loglevel=log.INFO, logstdout=True)
        crawler.crawl(spider)
        crawler.start()
        reactor.run()
    else:
        logger.info('Pending job found for spider {}'.format(spider_name))
        job = is_scraping

    return job.raw_response


@shared_task
def process_scrape(spider_name):
    """
    Process the results of a scrape for a spider.  Will read the JSONLines file and make the appropriate
    Raw objects in the database
    :param spider_name: str name of the spider that produced the results
    :return:
    """
    try:
        job = ScrapeJob.objects.latest_complete_job(spider_name)
    except ScrapeJob.DoesNotExist:
        logger.warn("No jobs found for spider {}".format(spider_name))
        return

    items_file = job.raw_response

    # Disable SQL logging
    if settings.DEBUG:
        original = BaseDatabaseWrapper.make_debug_cursor
        BaseDatabaseWrapper.make_debug_cursor = lambda self, cursor: CursorWrapper(cursor, self)

    # Get the processor and run it
    processor = processors.get_processor_for_spider(spider_name)
    logger.info('Processing file {} from ScrapeJob {}'.format(items_file, job.id))
    processor(items_file, job).process()

    if settings.DEBUG:
        BaseDatabaseWrapper.make_debug_cursor = original

    # Log that the job was processed just now
    job.last_fetched = datetime.now()
    job.save()
    return
