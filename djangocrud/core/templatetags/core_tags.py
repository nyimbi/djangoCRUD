import itertools
from collections import OrderedDict
from django import template

from djangocrud.core.constants import FIELD_CONFIG

register = template.Library()


def get_entity_data(instance, option):
    field_config = FIELD_CONFIG[type(instance).__name__]

    def compute(field_config):
        for field_name in field_config:
            if option in field_config[field_name]:
                yield field_name

    return OrderedDict([(field_name, getattr(
        instance, field_name)) for field_name in itertools.islice(
            compute(field_config), len(field_config))])


@register.filter(is_safe=True)
def label_with_class(value, arg):
    return value.label_tag(attrs={'class': arg})


@register.assignment_tag(takes_context=True)
def model_field_values(context, option):
    instance = context['object']

    return get_entity_data(instance, option)


@register.assignment_tag(takes_context=True)
def entity_preview(context):
    _parent = {}
    instances = context['objects']
    model = type(instances[0])

    for instance in instances:
        _parent[instance.id] = get_entity_data(
            instance, model, 'preview')

    return _parent


@register.assignment_tag
def entity_type(object):
    return type(object).__name__
