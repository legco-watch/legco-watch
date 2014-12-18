import logging
from django.db import models
from django.db.models import get_model
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


class ParsedMembership(TimestampMixin, BaseParsedModel):
    pass
