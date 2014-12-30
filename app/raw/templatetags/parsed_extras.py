from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from raw.models import BaseParsedModel


register = template.Library()

@register.filter
def link_model(val):
    # If val is a model instance, then return a link to that instance's model detail page
    if isinstance(val, BaseParsedModel):
        return mark_safe(u'<a href="{}">{}</a>'.format(reverse('parsed_model_detail', kwargs={'model': val._meta.model_name, 'uid': val.uid}), unicode(val)))
    else:
        return val