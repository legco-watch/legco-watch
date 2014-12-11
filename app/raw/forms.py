from django.forms import Form, BaseForm, fields_for_model, BooleanField


class OverrideForm(Form):
    deactivate = BooleanField()

    @classmethod
    def from_model_instance(cls, instance):
        # Create a Form from a raw model instance.  The form has fields for all of the fields in the model that are
        # overridable

        # First we get the fields for the model
        # if the model has `not_overridable`, then we exclude it from the list
        exclude = getattr(instance, 'not_overridable', [])
        # By default, we want to exclude things like last_crawled and the uid
        exclude.extend(['last_crawled', 'last_parsed', 'crawled_from', 'uid'])

        # Get the fields and attach it to the new form instance
        fields = fields_for_model(instance._meta.model, exclude=exclude)
        new_obj = cls()
        new_obj.fields = fields
        return new_obj

    @classmethod
    def from_parser_instance(cls, instance):
        # Parser classes don't have the same detailed field definitions as models
        pass
