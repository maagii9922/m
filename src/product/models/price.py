# -*- coding:utf-8 -*-

"""
Бүтээгдэхүүний үнэ
"""

from django.db import models

from src.company.models import Company
from src.warehouse.models import Warehouse
from src.product.models import Product


class Price(models.Model):
    """
    Бүтээгдэхүүний үнэ
    """
    company = models.ForeignKey(
        Company,
        verbose_name='Компани',
        on_delete=models.CASCADE,
        related_name='prices'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name='Агуулах',
        on_delete=models.CASCADE,
        related_name='prices'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Бүтээгдэхүүн',
        on_delete=models.CASCADE,
        related_name='prices'
    )
    price = models.FloatField(verbose_name='Үнэ')
    cost = models.FloatField(verbose_name='Өртөг', null=True, blank=True)
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
        verbose_name = 'Бүтээгдэхүүний үнэ'
        verbose_name_plural = 'Бүтээгдэхүүний үнүүд'

    def __str__(self):
        return self.product.name
