# -*- coding:utf-8 -*-

"""
Widget
"""

from django import forms
from django.shortcuts import reverse


class DateRangeInput(forms.TextInput):
    """
    DateRangeInput
    """

    class Media:
        css = {
            'all': ("https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css", )
        }
        js = (
            'https://cdn.jsdelivr.net/momentjs/latest/moment.min.js',
            'https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js',
            'employee/js/daterangepicker.js'
        )

    def __init__(self, attrs=None):
        default_attrs = {'data-toggle': 'daterangepicker'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    # def get_context(self, name, value, attrs):
    #     context = super().get_context(name, value, attrs)
    #     context['widget']['attrs'].update({'data-toggle': 'daterangepicker'})
    #     return context


class AutocompleteMixin:
    """
    Select widget mixin that loads options from AutocompleteJsonView via AJAX.

    Renders the necessary data attributes for select2 and adds the static form
    media.
    """

    def __init__(self, url, attrs=None, choices=()):
        self.choices = choices
        self.url = url
        self.db = None
        self.attrs = {} if attrs is None else attrs.copy()

    def get_url(self):
        return reverse(self.url)

    def build_attrs(self, base_attrs, extra_attrs=None):
        """
        Set select2's AJAX attributes.

        Attributes can be set using the html5 data attribute.
        Nested attributes require a double dash as per
        https://select2.org/configuration/data-attributes#nested-subkey-options
        """
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.setdefault('class', '')
        attrs.update({
            'data-ajax--url': self.get_url(),
            'class': attrs['class'] + (' ' if attrs['class'] else '') + 'form-contorl select2',
        })
        return attrs

    @property
    def media(self):
        return forms.Media(
            js=(
                # 'manager/lib/select2/js/select2.full.min.js',
                'employee/js/widgets/autocomplete.js',
            ),
            css={
                'all': (
                    # 'manager/lib/select2/css/select2.min.css',
                ),
            },
        )


class AutocompleteSelect(AutocompleteMixin, forms.Select):
    pass


class AutocompleteSelectMultiple(AutocompleteMixin, forms.SelectMultiple):
    pass
