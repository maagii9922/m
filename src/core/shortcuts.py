# -*- coding:utf-8 -*-

"""
Shortcuts
"""

from django.shortcuts import _get_queryset


def xstring(string):
    """
    Хоосон str байвал None болгоно
    """
    return None if string is '' else string


def get_object_or_none(cls, *args, **kwargs):
    """
    Обьект байвал дуудна байхгүй бол None буцаана
    """
    queryset = _get_queryset(cls)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_object_or_create(cls, *args, **kwargs):
    """
    Обьект байвал дуудна байхгүй бол шинэ обьект буцаана
    """
    queryset = _get_queryset(cls)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return cls(*args, **kwargs)
