# -*- coding:utf-8 -*-

"""
Сурталчилгаа админ
"""

from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """
    Сурталчилгаа
    """
