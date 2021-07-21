# -*- coding:utf-8 -*-

"""
Бүтээгдэхүүний хэмжих нэгж
"""

from django.db import models


class MeasuringType(models.Model):
    """
    Бүтээгдэхүүний хэмжих нэгж
    """
    name = models.CharField(verbose_name='Нэр', max_length=64)
    factor = models.FloatField()
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
        verbose_name = 'Хэмжих нэгж'
        verbose_name_plural = 'Хэмжих нэгжүүд'

    def __str__(self):
        return self.name
