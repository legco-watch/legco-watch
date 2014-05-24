"""
Trigger a crawl for a given spider in the project
"""
from django.utils.timezone import now
from django.conf import settings
from django.core.management import BaseCommand
import json
import urllib2
from raw.models import ScrapeJob


class Command(BaseCommand):
    args = '<spider_name spider_name ...>'
    help = 'Trigger a crawl on the scrapyd server, and store the JobId for retrieval later'

    def handle(self, *args, **options):
        schedule_url = '{}/schedule.json'.format(settings.SCRAPYD_SERVER)
        for spider in args:
            self.stdout.write("Scheduling spider: {}".format(spider))
            res = urllib2.urlopen(schedule_url, "project=legcoscraper&spider={}".format(spider))
            res = res.read()
            resp = json.loads(res)
            job = ScrapeJob.objects.create(
                spider=spider,
                scheduled=now(),
                job_id=resp['jobid'],
                raw_response=res
            )
            self.stdout.write(res)
