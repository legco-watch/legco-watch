"""
Run the processor for a given crawler.  Scrape job must be complete before
processing.
"""
from django.core.management import BaseCommand
from optparse import make_option
from raw import processors
from raw.models import ScrapeJob


class Command(BaseCommand):
    args = '<spider_name spider_name ...>'
    options_list = BaseCommand.option_list + (
        make_option('--force',
                    action='store_true',
                    dest='force',
                    default=False,
                    help="Reprocess a spider's last crawl job"),
    )
    help = 'Trigger a crawl on the scrapyd server, and store the JobId for retrieval later'

    def handle(self, *args, **options):
        for spider in args:
            self.handle_single_spider(spider, options.get('force', False))

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

        # Find the right processor
        processor = processors.get_processor_for_spider(spider)
