from django.forms import Form, BaseForm, fields_for_model, BooleanField


class OverrideForm(Form):
    deactivate = BooleanField()

    @classmethod
    def from_model(cls, instance):
        # Create a Form from a raw model instance.  The form has fields for all of the fields in the model that are
        # overridable

        # First we get the fields for the model
        # if the model has `not_overridable`, then we exclude it from the list
        exclude = getattr(instance, 'not_overridable', [])
        # By default, we want to exclude things like the uid
        exclude.extend(['created', 'modified', 'uid'])

        # Get the fields and attach it to the new form instance
        fields = fields_for_model(instance._meta.model, exclude=exclude)
        new_obj = cls()
        new_obj.fields = fields
        return new_obj
