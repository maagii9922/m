# -*- coding:utf-8 -*-

"""
Бүтээгдэхүүний хэлбэр
"""

from django.db import models


class Form(models.Model):
    """
    Бүтээгдэхүүний хэлбэр
    """
    name = models.CharField(max_length=64)
    flag = models.IntegerField()
    is_active = models.BooleanField(verbose_name='Идэвхитэй', default=True)
    created_at = models.DateTimeField(
        verbose_name='Үүссэн огноо',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Зассан огноо',
        auto_now=True
    )

    class Meta:
        ordering = ['-updated_at', 'id']
        verbose_name = 'Бүтээгдэхүүний хэлбэр'
        verbose_name_plural = 'Бүтээгдэхүүний хэлбэрүүд'

    def __str__(self):
        return self.name
