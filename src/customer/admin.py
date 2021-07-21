# -*- coding:utf-8 -*-

"""
Харилцагчийн админ
"""

from django.contrib import admin

from .models import CustomerCategory, Customer, CEOInformation


@admin.register(CustomerCategory)
class CustomerCategoryAdmin(admin.ModelAdmin):
    """
    Харилцагчийн төрөл админ
    """


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Харилцагчийн админ
    """
    list_display = ('name', 'company', 'phone', 'updated_at', )
    list_filter = ('company', )
    search_fields = ('id', 'name', 'phone', 'email',
                     'company__name', 'register_no')
    list_editable = ('phone', )


@admin.register(CEOInformation)
class CEOInformationAdmin(admin.ModelAdmin):
    pass
