from django.db import models


class ErrorReportManager(models.Manager):
    def open_errors(self):
        return self.filter(resolved=False)


class ErrorReport(models.Model):
    """
    Reports of inaccuracies in the data
    """
    # Timestamp of the when the report was created
    reported = models.DateTimeField()
    # The url of the page that the error is on
    url = models.TextField()
    # User comment
    comment = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)

    objects = ErrorReportManager()

    class Meta:
        ordering = ['-reported']

    def __unicode__(self):
        return self.reported.strftime('%Y-%m-%d %H:%M:%S')
