# -*- coding: utf-8 -*-

"""Компани админ"""

from django.contrib import admin

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    """
    Компанийн админ интерфейс удирдлага
    """
    search_fields = ('name', )
    list_display = ('name', 'partner_id', 'flag', 'created_at', 'updated_at')


admin.site.register(Company, CompanyAdmin)
