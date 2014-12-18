from django.forms import Form, BaseForm, fields_for_model, BooleanField


class OverrideForm(Form):
    deactivate = BooleanField()

    @classmethod
    def from_model(cls, instance, form_kwargs=None):
        # Create a Form from a model instance.  The form has fields for all of the fields in the model that are
        # overridable
        # Get the fields and attach it to the new form instance
        if form_kwargs is None:
            form_kwargs = {}
        fields = [xx.name for xx in instance.get_overridable_fields()]
        fields = fields_for_model(instance._meta.model, fields=fields)
        new_obj = cls(**form_kwargs)
        new_obj.fields = fields
        return new_obj
