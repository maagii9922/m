# -*- coding: utf-8 -*-

"""Агуулах модель"""

from django.db import models

from src.company.models import Company


class Warehouse(models.Model):
    """
    Агуулах
    """
    company = models.ForeignKey(
        Company,
        verbose_name='Компани',
        on_delete=models.CASCADE,
        related_name='warehouses'
    )
    name = models.CharField(verbose_name='Нэр', max_length=124)
    flag = models.IntegerField()
    is_active = models.BooleanField(verbose_name='Идэвхитэй', default=True)
    created_at = models.DateTimeField(
        verbose_name='Үүссэн огноо', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Зассан огноо', auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'id']
        verbose_name = 'Агуулах'
        verbose_name_plural = 'Агуулахууд'

    def __str__(self):
        return self.name
