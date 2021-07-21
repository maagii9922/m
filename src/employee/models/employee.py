# -*- coding:utf-8 -*-

"""
Ажилтан
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from src.company.models import Company
from src.warehouse.models import Warehouse
from src.employee.models import Position


class Employee(models.Model):
    """
    Ажилтан
    """
    GENDER_CHOICES = (
        (1, 'Эр'),
        (2, 'Эм'),
    )
    erp_id = models.IntegerField(null=True)
    user = models.OneToOneField(
        User,
        verbose_name='Хэрэглэгч',
        on_delete=models.CASCADE,
        null=True
    )
    company = models.ForeignKey(
        Company,
        verbose_name='Хариуцах компани',
        on_delete=models.CASCADE,
        related_name='employees',
        null=True,
        blank=True
    )
    warehouses = models.ManyToManyField(
        Warehouse,
        verbose_name='Хариуцах агуулахууд',
        blank=True
    )
    position = models.ForeignKey(
        Position,
        verbose_name='Албан тушаал',
        on_delete=models.CASCADE,
        related_name='employees',
        null=True,
        blank=True
    )
    family_name = models.CharField(
        verbose_name='Ургын овог',
        max_length=128,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Овог',
        max_length=128,
        null=True
    )
    first_name = models.CharField(
        verbose_name='Өөрийн нэр',
        max_length=128,
        null=True
    )
    register_no = models.CharField(
        verbose_name='Регистерийн дугаар',
        max_length=128,
        null=True
    )
    email = models.EmailField(verbose_name='Имэйл', null=True)
    phone = models.CharField(verbose_name='Утас', max_length=64, null=True)
    birth_date = models.CharField(
        verbose_name='Төрсөн огноо',
        max_length=62,
        null=True
    )
    gender = models.IntegerField(
        verbose_name='Хүйс',
        choices=GENDER_CHOICES,
        null=True
    )
    is_super_manager = models.BooleanField(
        verbose_name='Удирдлагын төлөв',
        help_text='Бүх компаний мэдээлэл харах боломжтой',
        default=False
    )
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
        verbose_name = 'Ажилтан'
        verbose_name_plural = 'Ажилтнууд'

    def __str__(self):
        return self.first_name

    def get_username(self):
        if self.user:
            return self.user.username
        return ''
    get_username.short_description = 'Нэвтрэх нэр'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    get_full_name.short_description = 'Овог/нэр'

    def get_position(self):
        if self.is_super_manager:
            return '<span class="badge badge-success">Админ</span>'
        return '<span class="badge badge-warning">Дотоод хэрэглэгч</span>'
    get_position.short_description = 'Хандах эрх'

    def get_action(self):
        if self.user:
            user_url = reverse_lazy(
                'employee-user-update', kwargs={'pk': self.user.pk})
        else:
            user_url = reverse_lazy(
                'employee-user-create', kwargs={'employee_pk': self.pk})
        return '''<div class = "dropdown">
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
                <a class="dropdown-item" href="{0}">Нэвтрэх нэр нууц үг</a>
                <a class="dropdown-item" href="{1}">Засах</a>
                <a class="dropdown-item" href="javascript:;" data-toggle="deleteAlert" data-href="{2}">Устгах</a>
              </div>
            </div>'''.format(
            user_url,
            reverse_lazy('employee-update', kwargs={'pk': self.pk}),
            reverse_lazy('employee-delete', kwargs={'pk': self.pk})
        )
