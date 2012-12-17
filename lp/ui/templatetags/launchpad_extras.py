from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def clean_isbn(value):
    isbn, sep, remainder = value.strip().partition(' ')
    if len(isbn) < 10:
        return ''
    for char in '-:.;':
        isbn = isbn.replace(char, '')
    return isbn


@register.filter
@stringfilter
def clean_issn(value):
    if len(value) < 9:
        return ''
    return value.strip().replace(' ', '-')


@register.filter
@stringfilter
def clean_oclc(value):
    if len(value) < 8:
        return ''
    return ''.join([c for c in value if c.isdigit()])


@register.filter
@stringfilter
def cjk_info(value):
    fields = value.split(' // ')
    field_partitions = [f.partition(' ') for f in fields]
    cjk = {}
    for field, sep, val in field_partitions:
        if field.startswith('1'):
            cjk['AUTHOR'] = val
        elif field.startswith('245'):
            cjk['TITLE'] = val
        elif field.startswith('260'):
            cjk['IMPRINT'] = val
        elif field.startswith('600'):
            cjk['AUTHOR600'] = val
    return cjk


@register.filter
@stringfilter
def noscream(value):
    for scream, calm in settings.SCREAMING_LOCATIONS:
        if scream in value:
            value = value.replace(scream, calm)
    return value


@register.filter
def remove_empty_links(marc856list):
    return [link_dict for link_dict in marc856list if link_dict.get('u', None)]


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, '')
