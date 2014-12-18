from datetime import datetime
import json
import logging
from django.db import models
from django.db.models import get_model
import re
from constants import GENDER_CHOICES
from .raw import RawMember


logger = logging.getLogger('legcowatch')


class TimestampMixin(object):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class BaseParsedModel(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    deactivate = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'raw'

    def get_overridable_fields(self):
        # First we get the fields for the model
        # if the model has `not_overridable`, then we exclude it from the list
        exclude = getattr(self, 'not_overridable', [])
        # By default, we want to exclude things like the uid
        exclude.extend(['created', 'modified', 'uid', 'id'])
        # Now iterate over the model fields to get the field names we want
        fields = []
        for field in self._meta.concrete_fields:
            if field.name not in exclude:
                fields.append(field)
        return fields


class OverrideManager(models.Manager):
    def get_from_reference(self, reference):
        # Tries to retrieve the override for a specific model instance
        model = reference._meta.model_name
        ref_uid = reference.uid
        try:
            return self.get(ref_model=model, ref_uid=ref_uid)
        except self.model.DoesNotExist as e:
            return None

    def get_for_class(self, class_name):
        # Retrieves all of the overrides for a specific model
        return self.filter(ref_model=class_name.lower())

    def create_from(self, reference):
        # Creates an uncommitted override for the reference
        model = reference._meta.model_name
        ref_uid = reference.uid
        instance = self.model(ref_model=model, ref_uid=ref_uid)
        return instance


class Override(models.Model):
    # The lowercase string name of the model we're referencing, model._meta.model_name
    ref_model = models.CharField(max_length=100, null=False)
    # The uid of the object we are overriding
    # Don't refer to id, because we want to be able to still look up
    # The reference if it is recreated and gets a new auto id
    ref_uid = models.CharField(max_length=100, unique=True)
    # Where the serialized override data is stored
    data = models.TextField(blank=True, null=False, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = OverrideManager()

    class Meta:
        app_label = 'raw'

    def __unicode__(self):
        return u'{} {}'.format(self.ref_model, self.ref_uid)

    def _get_model(self):
        # Gets the model class from the string name
        # We assume all of the models are in the Raw app
        res = get_model('raw', self.ref_model)
        return res

    def get_reference(self):
        # Gets the reference object
        model = self._get_model()
        try:
            instance = model.objects.get(id=self.ref_uid)
        except model.DoesNotExist as e:
            logger.warn('Instance of {} with id {} does not exist'.format(self.ref_model, self.ref_uid))
            return None
        return instance


class PersonManager(models.Manager):
    def create_from_raw(self, raw_obj):
        try:
            obj = self.get(uid=raw_obj.uid)
        except self.model.DoesNotExist as e:
            obj = self.model()
        # Copy items over
        for field in [xx.name for xx in obj._meta.fields]:
            setattr(obj, field, getattr(raw_obj, field, None))
        obj.deactivate = False
        return obj

    def populate(self):
        raw_items = RawMember.objects.all()
        for item in raw_items:
            # Get or create, but without commit
            obj = self.create_from_raw(item)
            obj.save()


class ParsedPerson(TimestampMixin, BaseParsedModel):
    name_e = models.CharField(max_length=100)
    name_c = models.CharField(max_length=100)
    title_e = models.CharField(max_length=100)
    title_c = models.CharField(max_length=100)
    honours_e = models.CharField(max_length=50, blank=True)
    honours_c = models.CharField(max_length=50, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    year_of_birth = models.IntegerField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=50, blank=True)
    homepage = models.TextField(blank=True)
    photo_file = models.TextField(blank=True)

    objects = PersonManager()

    not_overridable = ['photo_file']

    def __unicode__(self):
        return u"{} {}".format(unicode(self.name_e), unicode(self.name_c))


class MembershipManager(models.Manager):
    def create_from_raw(self, raw_obj):
        # Create all the memberships from a RawMember.  So could result in multiple new objects
        try:
            obj = self.get(uid=raw_obj.uid)
        except self.model.DoesNotExist as e:
            obj = self.model()
        # Copy items over
        for field in [xx.name for xx in obj._meta.fields]:
            setattr(obj, field, getattr(raw_obj, field, None))
        obj.deactivate = False
        return obj

    def populate(self):
        raw_items = RawMember.objects.all()
        for item in raw_items:
            parsed = MembershipParser(item.service_e)


class ParsedMembership(TimestampMixin, BaseParsedModel):
    person = models.ForeignKey(ParsedPerson, related_name='memberships')
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)
    method_obtained = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    note = models.CharField(max_length=255, default='')

    objects = PersonManager()

    not_overridable = ['person']


class MembershipParser(object):
    # Container for parsing membership data in RawMember.service_e and service_c
    # We only care about the English, and we'll use that as the basis for translation into Chinese
    DATE_RE = r'(?P<start>\d+ \w+ \d+) - (?P<end>\d+ \w+ \d+)?'
    DETAIL_RE = r'^(?P<method>\w+) \((?P<position>[a-zA-Z\- ]+)\)$'
    DATE_FORMAT = '%d %B %Y'

    def __init__(self, membership_obj, lang='E'):
        self._raw = membership_obj
        self.start_date, self.end_date = self.parse_dates(membership_obj[0])
        method, position = self.parse_position_method(membership_obj[1])
        # Appointed or Elected
        self.method_obtained = method
        # Ex Officio - Chief Secretary, Geographical Constituency - Kowloon East
        self.position = position
        # Retired, replaced, resigned, etc.
        if len(membership_obj) > 2:
            self.note = self.parse_note(membership_obj[2])
        else:
            self.note = None

    def parse_date(self, date_str):
        if date_str is None:
            return None
        try:
            return datetime.strptime(date_str, self.DATE_FORMAT).date()
        except ValueError:
            return None

    def parse_dates(self, date_string):
        # First element of the json object is the string
        matched_dates = re.match(self.DATE_RE, date_string)
        if matched_dates is None:
            return None, None

        matches = matched_dates.groups()
        return self.parse_date(matches[0]), self.parse_date(matches[1])

    def parse_position_method(self, position_string):
        matched = re.match(self.DETAIL_RE, position_string)
        if matched is None:
            return None, None

        groups = matched.groups()
        return groups[0], groups[1]

    def parse_note(self, note_string):
        res = note_string.replace('(', '').replace(')', '')
        return res


def foo():
    from raw import models
    import json, itertools
    services = [json.loads(xx.service_e) for xx in models.RawMember.objects.all()]
    services = list(itertools.chain.from_iterable(services))
