# -*- coding: utf-8 -*-

"""Агуудах админ"""

from django.contrib import admin

from .models import Warehouse


class WarehouseAdmin(admin.ModelAdmin):
    """
    Агуулах админ
    """
    list_display = ('name', 'company', 'created_at', 'updated_at')
    list_filter = ('company__name', )
    search_fields = ('name', )


admin.site.register(Warehouse, WarehouseAdmin)
