"""
Trigger a crawl for a given spider in the project
"""
from django.utils.timezone import now
from django.conf import settings
from django.core.management import BaseCommand
import json
import urllib2
import urlparse
from raw.models import ScrapeJob


# Note that it is possible to trigger a crawl on a spider that doesn't exist.
# This will cause an error on the scrapyd server, but we otherwise have no way of knowing
class Command(BaseCommand):
    args = '<spider_name spider_name ...>'
    help = 'Trigger a crawl on the scrapyd server, and store the JobId for retrieval later'

    def handle(self, *args, **options):
        schedule_url = urlparse.urljoin(settings.SCRAPYD_SERVER, 'schedule.json')
        for spider in args:
            self.stdout.write("Scheduling spider: {}".format(spider))
            res = urllib2.urlopen(schedule_url, "project=legcoscraper&spider={}".format(spider))
            res = res.read()
            try:
                resp = json.loads(res)
            except ValueError:
                self.stdout.write("Error on scrapyd server:")
                self.stdout.write(res)
                return

            job = ScrapeJob.objects.create(
                spider=spider,
                scheduled=now(),
                job_id=resp['jobid'],
                raw_response=res
            )
            self.stdout.write(res)
