# -*- coding:utf-8 -*-

"""
Core nice url
"""
import re
from importlib import import_module

from django.urls import path


class NiceUrl(object):
    """
    Usage:
    * NiceUrl(r'example-url')    > 'app.path.to.view',
    * NiceUrl(r'example-prefix') > include('app.path.to.urls'),
    Feature:
    - Automatic name support ::
        NiceUrl(r'example-url') > 'app.app_label.views.ExamplePage'
        equal to:
        url(r'example-url', name='app_label-example-page', ExamplePage.as_view())
    """

    def __init__(self, regex, kwargs=None, name=None, prefix=''):
        self.regex = regex
        self.kwargs = kwargs
        self.name = name
        self.prefix = prefix

    def _import_view(self, view):
        """
        :input: "path.app.views.Hello"
        :return: <function Hello.as_view()>
        """
        mod_name = view.rsplit('.', 1)[0]
        class_name = view.rsplit('.', 1)[1]
        view_class = getattr(import_module(mod_name), class_name)

        return view_class.as_view()

    def _get_name(self, view):
        """
        :input: "app.{path}.views.Hello"
        :return: "{path}-hello"
        """
        view_name = view.rsplit('.')[-1]

        app_path = view[:-len(view_name)][:-len('.views')][len('src.'):]
        app_path = app_path.replace('.', '-')

        # Camelcase convert
        view_name = re.sub('(.)([A-Z][a-z]+)', r'\1%s\2' % '-', view_name)
        view_name = re.sub('([a-z0-9])([A-Z])', r'\1%s\2' %
                           '-', view_name).lower()

        return '%s%s' % (app_path, view_name)

    def __gt__(self, view):
        if not isinstance(view, str):
            return path(self.regex, view.as_view(), kwargs=self.kwargs, name=self.name)
            # raise Exception('NiceUrl only support string')

        self.name = self.name or self._get_name(view)

        # if is CBV
        if view.rsplit('.', 1)[1][0].isupper():
            # import module
            view = self._import_view(view)

        self.view = view

        return path(self.regex, self.view, kwargs=self.kwargs, name=self.name)


Nurl = NiceUrl
