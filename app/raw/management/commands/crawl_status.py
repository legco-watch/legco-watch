"""
For each ScrapeJob that is not registered as completed, query the scrapyd server for it status
"""
from datetime import datetime
from django.core.management import BaseCommand
import json
import urllib2
import urlparse
from legcowatch import settings
from raw.models import ScrapeJob
import pytz


class Command(BaseCommand):
    help = 'Get the status of crawl jobs'

    def handle(self, *args, **options):
        schedule_url = urlparse.urljoin(settings.SCRAPYD_SERVER, 'listjobs.json')
        # Get the jobs that have not been completed
        incomplete_jobs = ScrapeJob.objects.pending_jobs()
        if len(incomplete_jobs) == 0:
            self.stdout.write("No pending jobs")
            return

        self.stdout.write("Fetching jobs status")
        res = urllib2.urlopen(schedule_url + "?project=legcoscraper")
        res = res.read()
        resp = json.loads(res)
        # resp is a JSON object with keys 'running', 'finished', and 'pending'
        finished_jobs = dict((xx['id'], xx) for xx in resp['finished'])
        for job in incomplete_jobs:
            finished_data = finished_jobs.get(job.job_id, None)
            if finished_data is None:
                self.stdout.write("Job {} still pending".format(job.job_id))

            completed_time = datetime.strptime(finished_data['end_time'], '%Y-%m-%d %H:%M:%S.%f')
            completed_time.replace(tzinfo=pytz.UTC)
            self.stdout.write("Job {} completed at {}".format(job.job_id, completed_time))
            job.completed = completed_time
            job.save()
