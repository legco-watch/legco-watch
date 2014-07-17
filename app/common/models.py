from django.db import models


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
