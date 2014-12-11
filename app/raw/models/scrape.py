from django.db import models


class ScrapeJobManager(models.Manager):
    def pending_jobs(self):
        """
        Returns the jobs that are still at the scraper
        """
        return self.filter(completed=None)

    def complete_jobs(self):
        """
        Jobs that have been completed
        """
        return self.exclude(completed=None)

    def latest_complete_job(self, spider):
        """
        Latest complete job for a single spider
        """
        return self.filter(spider=spider).exclude(completed=None).latest('completed')

    def unprocessed_jobs(self):
        """
        Returns jobs that have been completed by the scraper, but have not yet been loaded
        into the raw models.  There may be more than one job per spider
        """
        return self.exclude(completed=None).filter(last_fetched=None).order_by('-completed')

    def latest_unprocessed_job(self, spider):
        """
        Gets the latest unprocessed job for a single spider
        """
        return self.filter(spider=spider).exclude(completed=None).filter(last_fetched=None).latest('completed')

    def orphaned_jobs(self):
        """
        Returns jobs that are somehow malformed.  This includes jobs:
          - That are marked as completed but do not have a corresponding items file on disk
        """
        pass


class ScrapeJob(models.Model):
    """
    Details for keeping track of a scrape job
    """
    spider = models.CharField(max_length=100)
    scheduled = models.DateTimeField()
    job_id = models.CharField(max_length=100)
    raw_response = models.TextField()
    completed = models.DateTimeField(null=True, blank=True)
    last_fetched = models.DateTimeField(null=True, blank=True)

    objects = ScrapeJobManager()

    def __unicode__(self):
        return u"{}: {}".format(self.spider, self.job_id)

    class Meta:
        app_label = 'raw'
