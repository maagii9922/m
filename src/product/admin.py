# -*- coding:utf-8 -*-

""" Product Admin File """

from django.contrib import admin


from .models import (Category, MeasuringType, Form, Product, Price, Stock)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category Admin
    """
    list_display = ('name', 'parent', 'flag', 'updated_at')


@admin.register(MeasuringType)
class MeasuringTypeAdmin(admin.ModelAdmin):
    """
    MeasuringType Admin
    """
    list_display = ('name', 'flag', 'updated_at')


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    """
    Form Admin
    """
    list_display = ('name', 'flag', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product Admin
    """
    list_display = ('name', 'category', 'measuring_type',
                    'form', 'updated_at')
    list_filter = ('category', )
    search_fields = ('name', 'category__name', 'internal_code')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """
    Stock Admin
    """
    list_display = ('warehouse', 'product', 'updated_at')
    search_fields = ('product__name',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    """
    Price Admin
    """
    search_fields = ('product__name', )
    list_display = ('company', 'warehouse', 'product', 'price', 'cost')
    list_filter = ('company', )
