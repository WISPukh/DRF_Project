from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
def get_verbose_field_name(instance):
    exclude_field = (
        'content_type',
        'product_ptr',
        'id',
        'img'
    )
    for name in instance._meta.fields:
        if name.name not in exclude_field:
            yield _(name.verbose_name), _(name.value_to_string(instance))