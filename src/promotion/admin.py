# -*- coding:utf-8 -*-

from django.contrib import admin

from src.promotion.models import Promotion, PromotionProduct


class PromotionProductTabularInline(admin.TabularInline):
    model = PromotionProduct
    extra = 1


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    inlines = [PromotionProductTabularInline]


@admin.register(PromotionProduct)
class PromotionProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['product']
