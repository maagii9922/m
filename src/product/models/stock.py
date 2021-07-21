# -*- coding:utf-8 -*-

"""
Бүтээгдэхүүний нөөц
"""

from django.db import models

from src.warehouse.models import Warehouse
from src.product.models import Product


class Stock(models.Model):
    """
    Бүтээгдэхүүний нөөц
    """
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name='Агуулах',
        on_delete=models.CASCADE,
        related_name='stocks'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Бүтээгдэхүүн',
        on_delete=models.CASCADE,
        related_name='stocks'
    )
    in_stock = models.FloatField(verbose_name='Барааны тоо хэмжээ')
    lot_name = models.CharField(
        verbose_name='Цувралын дугаар',
        max_length=128,
        null=True,
        blank=True
    )
    expiration_date = models.DateTimeField(
        verbose_name='Дуусах хугацаа',
        null=True,
        blank=True
    )
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
        verbose_name = 'Бүтээгдэхүүн нөөц'
        verbose_name_plural = 'Бүтээгдэхүүн нөөцүүд'

    def __str__(self):
        return self.product.name
