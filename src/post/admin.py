# -*- coding:utf-8 -*-

"""
Post admin
"""

from django.contrib import admin

from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin
    """


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Tag admin
    """


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post admin
    """
