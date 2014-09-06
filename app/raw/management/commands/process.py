"""
Run the processor for a given crawler.  Scrape job must be complete before
processing.
"""
from django.conf import settings
from django.core.management import BaseCommand
from django.db.backends import BaseDatabaseWrapper
from django.db.backends.util import CursorWrapper
from optparse import make_option
import os
from raw import processors
from raw.models import ScrapeJob


class Command(BaseCommand):
    args = '<spider_name spider_name ...>'
    option_list = BaseCommand.option_list + (
        make_option('--force',
                    action='store_true',
                    dest='force',
                    default=False,
                    help="Reprocess a spider's last crawl job"),
        make_option('--items_file',
                    action='store',
                    dest='items_file',
                    type='string',
                    help="Process this Items file instead of looking in the ScrapeJobs database"),
    )
    help = 'Process the results of a crawl'

    def handle(self, *args, **options):
        # Disable DB debug messages temporarily
        if settings.DEBUG:
            original = BaseDatabaseWrapper.make_debug_cursor
            BaseDatabaseWrapper.make_debug_cursor = lambda self, cursor: CursorWrapper(cursor, self)
        if len(args) == 0:
            raise RuntimeError('You must provide a spider name to process the results.')
        items_file = options.get('items_file', None)
        if items_file is not None:
            if not os.path.exists(items_file):
                raise RuntimeError("The file {} does not seem to exist".format(items_file))
            self._process_items_file(args[0], items_file)
        else:
            for spider in args:
                self.handle_single_spider(spider, options.get('force', False))
        if settings.DEBUG:
            BaseDatabaseWrapper.make_debug_cursor = original

    def handle_single_spider(self, spider, force=False):
        # Get the path to the Items file
        # Instantiate the relevant processor script with the Items file
        try:
            if force:
                job = ScrapeJob.objects.latest_complete_job(spider)
            else:
                job = ScrapeJob.objects.latest_unprocessed_job(spider)
        except ScrapeJob.DoesNotExist:
            self.stdout.write("No jobs found for spider {}".format(spider))
            return

        # Try to find the resulting items file
        try:
            items_file = processors.get_items_file(spider, job.job_id)
        except RuntimeError as e:
            self.stdout.write("Could not find items file for spider {}, job {}: {}".format(spider, job.job_id, e))
            return

        self._process_items_file(spider, items_file, job)

    def _process_items_file(self, spider, items_file, job=None):
        # Find the right processor
        processor = processors.get_processor_for_spider(spider)
        processor(items_file, job).process()
