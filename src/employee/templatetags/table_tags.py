"""
Table tags
"""

from django import template
from django.core.exceptions import FieldDoesNotExist

register = template.Library()


@register.inclusion_tag('employee/core/template_tag/table.html', takes_context=True)
def table(context):
    """
    table
    """
    request = context.get('request')
    filter_form = context.get('filter_form')
    object_list = context.get('object_list')
    page_obj = context.get('page_obj')
    is_paginated = context.get('is_paginated')
    fields = context.get('fields')

    headers = get_headers(object_list.model, fields)
    filter_form = get_filter_form(filter_form)
    rows = get_rows(object_list, fields)

    return {
        'request': request,
        'headers': headers,
        'filter_form': filter_form,
        'rows': rows,
        'is_paginated': is_paginated,
        'page_obj': page_obj,
    }


def get_headers(model, fields):
    """
    headers
    """
    for field in fields:
        try:
            label = model._meta.get_field(field).verbose_name
        except FieldDoesNotExist:
            attr = getattr(model, field)
            if hasattr(attr, 'short_description'):
                label = getattr(attr, 'short_description')
            else:
                label = ''
        yield label


def get_filter_form(filter_form):
    """
    filter_form
    """
    return filter_form


def get_rows(object_list, fields):
    """
    rows
    """
    model = object_list.model
    fields_names = [field.name for field in model._meta.get_fields()]
    for obj in object_list:
        values = []
        for field in fields:
            if field in fields_names:
                values.append(getattr(obj, field))
            else:
                values.append(getattr(obj, field)())
        if hasattr(obj, 'get_action'):
            values.append(getattr(obj, 'get_action')())
        else:
            values.append('')
        yield values


@register.inclusion_tag('employee/core/template_tag/pagination.html', takes_context=True)
def end_pagination(context, page, begin_pages=2, end_pages=2, before_current_pages=4, after_current_pages=4):
    """
    return google like pagination
    Usage::
        {% load end_tags %}
        {% end_pagination the_obj_to_paginate %}

    Example::
        {% end_pagination page_obj %}
    At this case page_obj is the defaul
    object for pages that django provide
    """
    request = context.get('request')

    before = max(page.number - before_current_pages - 1, 0)
    after = page.number + after_current_pages

    begin = page.paginator.page_range[:begin_pages]
    middle = page.paginator.page_range[before:after]
    end = page.paginator.page_range[-end_pages:]
    last_page_number = end[-1]

    def collides(firstlist, secondlist):
        """ 
        Returns true if lists collides (have same entries)
        Example::
        >>> collides([1,2,3,4],[3,4,5,6,7])
        True
        >>> collides([1,2,3,4],[5,6,7])
        False
        """
        return any(item in secondlist for item in firstlist)

    # If middle and end has same entries, then end is what we want
    if collides(middle, end):
        end = range(max(last_page_number - before_current_pages - after_current_pages, 1), last_page_number + 1)  # noqa
        middle = []

    # If begin and middle ranges has same entries, then begin is what we want
    if collides(begin, middle):
        begin = range(1, min(before_current_pages + after_current_pages, last_page_number) + 1)  # noqa
        middle = []

    # If begin and end has the same entries then begin is what we want
    if collides(begin, end):
        begin = range(1, last_page_number + 1)
        end = []

    return {
        'request': request,
        'page': page,
        'begin': begin,
        'middle': middle,
        'end': end
    }
