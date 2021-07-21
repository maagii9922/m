# -*- coding:utf-8 -*-

"""
Employee admin
"""

from django.contrib import admin

from .models import Position, Employee


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'flag', 'updated_at')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'position',
                    'company', 'erp_id', 'updated_at')
