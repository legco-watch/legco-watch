from django.db import models

"""
Core LegCo models

Not quite sure how to handle panels and committees yet
"""


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimestampedModel):
    """
    """
    pass


class Council(TimestampedModel):
    """
    For example, then 5th Legislative Council
    """
    pass


class Session(TimestampedModel):
    """
    LegCo sessions, for example, the 2013/2014 session
    Belongs to a Council
    """
    pass


class Constituency(TimestampedModel):
    """
    Functional and geographic constituencies
    """
    pass


class Membership(TimestampedModel):
    """
    Essentially an elected seat within a LegCo session.
    Should have start date and end date, to account for the possiblity
    of a membership that ends in a certain date
    """
    pass


class Meeting(TimestampedModel):
    """
    A meeting instance
    """
    pass
