# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.translation import ugettext as _


def log_create(request, object):
    """
    Амжилттай обьект нэмэгдэх үед Лог бичигдэнэ.
    LogEntry моделд обьект нэмэгдэнэ.
    """
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=ADDITION,
        change_message=_('Created')
    )


def log_update(request, object):
    """
    Амжилттай обьект засагдах үед Лог бичигдэнэ.
    LogEntry моделд обьект нэмэгдэнэ.
    """
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=CHANGE,
        change_message=_('Updated')
    )


def log_delete(request, object):
    """
    Амжилттай обьект устгагдах үед Лог бичигдэнэ.
    LogEntry моделд обьект нэмэгдэнэ.
    """
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=DELETION,
        change_message=_('Deleted')
    )
