# -*- coding:utf-8 -*-

"""
Сурталчилгаа модель
"""

from django.db import models
from django.urls import reverse_lazy

from src.warehouse.models import Warehouse
from src.customer.models import CustomerCategory, Customer


class Advertisement(models.Model):
    """
    Сурталчилгаа
    """
    IMPLEMENT_TYPE = (
        (1, 'Бүгд'),
        (2, 'Харилчагчийн төрөл'),
        (3, 'Харилцагчид'),
        (4, 'Агуулах'),
    )
    name = models.CharField(verbose_name='Нэр', max_length=256)
    image = models.ImageField(
        verbose_name='Баннер зураг',
        upload_to='advertisement'
    )
    description = models.TextField(
        verbose_name='Тайлбар',
        null=True,
        blank=True
    )
    implement_type = models.IntegerField(
        verbose_name='Хэрэгжүүлэх төрөл',
        choices=IMPLEMENT_TYPE
    )
    customer_categories = models.ManyToManyField(
        CustomerCategory,
        related_name='advertisements',
        verbose_name='Харилцагчийн төрөл',
        blank=True
    )
    customers = models.ManyToManyField(
        Customer,
        related_name='advertisements',
        verbose_name='Харилцагчид',
        blank=True
    )
    warehouses = models.ManyToManyField(
        Warehouse,
        related_name='advertisements',
        verbose_name='Агуулах',
        blank=True
    )
    is_implement = models.BooleanField(
        verbose_name='Хэрэгжүүлэх эсэх', default=True)
    is_active = models.BooleanField(verbose_name='Идэвхитэй', default=True)
    created_at = models.DateTimeField(
        verbose_name='Үүссэн огноо', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Зассан огноо', auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'id']
        verbose_name = 'Сурталчилгаа'
        verbose_name_plural = 'Сурталчилгаанууд'

    def __str__(self):
        return self.name

    def get_implement_type(self):
        return self.get_implement_type_display()
    get_implement_type.short_description = 'Хэрэгжүүлэх төрөл'

    def get_action(self):
        return '''
            <div class = "dropdown">
              <button class = "btn btn-white btn-xs dropdown-toggle" type = "button"
                id = "dropdownMenuButton"
                data-toggle = "dropdown"
                aria-haspopup = "true"
                aria-expanded = "false" >
                <i data-feather = "settings"></i>
                Тохиргоо
              </button>
              <div class = "dropdown-menu"
                aria-labelledby = "dropdownMenuButton">
                <a href="javascript:;" class="dropdown-item detailInformation" data-href="{0}">Дэлгэрэнгүй</a>
                <a href="javascript:;" class="dropdown-item detailInformation" data-href="{1}">Өөрчлөлтийн түүх</a>
                <a class="dropdown-item" href="{2}">Засах</a>
                <a class="dropdown-item" href="javascript:;" data-toggle="deleteAlert" data-href="{3}">Устгах</a>
              </div>
            </div>'''.format(
            reverse_lazy('employee-advertisement-detail',
                         kwargs={'pk': self.pk}),
            reverse_lazy('employee-advertisement-history',
                         kwargs={'pk': self.pk}),
            reverse_lazy('employee-advertisement-update',
                         kwargs={'pk': self.pk}),
            reverse_lazy('employee-advertisement-delete',
                         kwargs={'pk': self.pk})
        )
