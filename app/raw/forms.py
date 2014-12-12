from django.forms import Form, BaseForm, fields_for_model, BooleanField


class OverrideForm(Form):
    deactivate = BooleanField()

    @classmethod
    def from_model(cls, instance):
        # Create a Form from a raw model instance.  The form has fields for all of the fields in the model that are
        # overridable
        # Get the fields and attach it to the new form instance
        fields = [xx.name for xx in instance.get_overridable_fields()]
        fields = fields_for_model(instance._meta.model, fields=fields)
        new_obj = cls()
        new_obj.fields = fields
        return new_obj
