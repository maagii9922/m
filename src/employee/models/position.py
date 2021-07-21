# -*- coding:utf-8 -*-

"""
Албан тушаал
"""

from django.db import models


class Position(models.Model):
    """
    Албан тушаал
    """
    name = models.CharField(verbose_name='Нэр', max_length=128)
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
        verbose_name = 'Албан тушаал'
        verbose_name_plural = 'Албан тушаалууд'

    def __str__(self):
        return self.name
