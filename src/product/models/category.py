# -*- coding:utf-8 -*-

"""
Бүтээгдэхүүн ангилал
"""

from django.db import models


class Category(models.Model):
    """
    Бүтээгдэхүүн ангилал
    """
    parent = models.ForeignKey(
        'Category',
        verbose_name='Ангилал',
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True
    )
    name = models.CharField(verbose_name='Нэр', max_length=128)
    flag = models.IntegerField(verbose_name='Флаг')
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
        verbose_name = 'Ангилал'
        verbose_name_plural = 'Ангиллууд'

    def __str__(self):
        return self.name
