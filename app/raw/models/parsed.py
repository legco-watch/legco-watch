import logging
from django.db import models
from django.db.models import get_model
from constants import GENDER_CHOICES


logger = logging.getLogger('legcowatch')


class TimestampMixin(object):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class BaseParsedModel(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    deactivate = models.BooleanField(default=0)
    # Store the override directly on the model
    override = models.TextField(blank=True, default='')

    class Meta:
        abstract = True
        app_label = 'raw'


class OverrideManager(models.Manager):
    def get_from_reference(self, reference):
        # Tries to retrieve the override for a specific model instance
        model = reference._meta.model_name
        ref_id = reference.id
        try:
            return self.get(ref_model=model, ref_id=ref_id)
        except self.model.DoesNotExist as e:
            return None

    def get_for_class(self, class_name):
        # Retrieves all of the overrides for a specific model
        return self.filter(ref_model=class_name.lower())

    def create_from(self, reference):
        # Creates an uncommitted override for the reference
        model = reference._meta.model_name
        ref_id = reference.id
        instance = self.model(ref_model=model, ref_id=ref_id)
        return instance


class Override(models.Model):
    # The lowercase string name of the model we're referencing, model._meta.model_name
    ref_model = models.CharField(max_length=100, null=False)
    # The id of the object we are overriding
    ref_id = models.IntegerField(null=False)
    # Where the serialized override data is stored
    data = models.TextField(blank=True, null=False, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = OverrideManager()

    class Meta:
        app_label = 'raw'

    def __unicode__(self):
        return u'{} {}'.format(self.ref_model, self.ref_id)

    def _get_model(self):
        # Gets the model class from the string name
        # We assume all of the models are in the Raw app
        res = get_model('raw', self.ref_model)
        return res

    def get_reference(self):
        # Gets the reference object
        model = self._get_model()
        try:
            instance = model.objects.get(id=self.ref_id)
        except model.DoesNotExist as e:
            logger.warn('Instance of {} with id {} does not exist'.format(self.ref_model, self.ref_id))
            return None
        return instance


class PersonManager(models.Manager):
    def populate(self):
        # Populate this table from the raw models
        pass


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

    def __unicode__(self):
        return u"{} {}".format(unicode(self.name_e), unicode(self.name_c))
