# -*- coding: utf-8 -*-

"""Компанийн мэдээлэл"""

from django.db import models


class Company(models.Model):
    """
    Компанийн мэдээлэл
    """
    partner_id = models.IntegerField(
        verbose_name='ИРП харилцагчийн ID',
        unique=True
        )
    name = models.CharField(verbose_name='Компанийн нэр', max_length=250)
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
        verbose_name = 'Компани'
        verbose_name_plural = 'Компаниуд'

    def __str__(self):
        return self.name
