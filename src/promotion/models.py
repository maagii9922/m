# -*- coding:utf-8 -*-

"""
Урамшууллын хүснэгт
"""

from django.db import models

# from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse_lazy

from src.core import constant as const
from src.core.validate import validate_nonzero
from src.warehouse.models import Warehouse
from src.product.models import Product
from src.customer.models import CustomerCategory, Customer

#     ('Үндсэн үнээс', True),
#     ('Хямдарсан үнээс', False),

#     ('Хэрэгжүүлэх', True),
#     ('Хэрэгжүүлэхгүй', False),

#     ('Авах', True),
#     ('Бонус', False),


class Promotion(models.Model):
    """
    Урамшуулал
    """

    name = models.CharField(verbose_name="Нэр", max_length=256)
    start_date = models.DateTimeField(verbose_name="Урамшуулал эхлэх огноо")
    end_date = models.DateTimeField(verbose_name="Урамшуулал дуусах огноо")
    calculation_type = models.BooleanField(verbose_name="Тооцоолох төрөл", default=True)
    order = models.PositiveIntegerField(verbose_name="Хэрэгжүүлэх дараалал")
    description = models.TextField(verbose_name="Тайлбар", null=True, blank=True)
    ############################################################
    promotion_type = models.IntegerField(
        verbose_name="Урамшууллын төрөл", choices=const.PROMOTION_TYPE
    )
    ############################################################
    product_type = models.IntegerField(
        verbose_name="Бүтээгдэхүүнд хэрэгжих", choices=const.PRODUCT_TYPE, null=True
    )
    ############################################################
    products = models.ManyToManyField(
        Product, verbose_name="Бүтээгдэхүүн", blank=True, related_name="promotions"
    )
    ############################################################
    promotion_implement_type = models.IntegerField(
        verbose_name="Урамшуулал хэрэгжих төрөл",
        choices=const.PROMOTION_IMPLEMENT_TYPE,
        null=True,
    )
    above_the_price = models.PositiveIntegerField(
        verbose_name="Үнийн дүнгээс дээш",
        null=True,
        blank=True,
        help_text="Тухайн үнээс дээш худалдан авалт хийсэн үед урамшуулал хэрэгжинэ",
    )
    percent = models.FloatField(
        verbose_name="Хувь",
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(99.9)],
    )
    price = models.FloatField(
        verbose_name="Үнэ", null=True, blank=True, validators=[MinValueValidator(0.1)],
    )
    above_the_number = models.IntegerField(
        verbose_name="Тооноос дээш",
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    supplier = models.ForeignKey(
        Customer,
        verbose_name="Нийлүүлэгч",
        on_delete=models.CASCADE,
        related_name="supplier_promotions",
        null=True,
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Багцийн тоо хэмжээ",
        null=True,
        validators=[validate_nonzero],
        help_text="Дээрхид утга оруулснаар багцад хамаарах бүтээгдэхүүнүүдийн нийт тоо хэмжээ хүрэх үед урамшуулал хэрэгжинэ",
    )
    ############################################################
    implement_type = models.IntegerField(
        verbose_name="Харилцагчид хэрэгжүүлэх төрөл", choices=const.IMPLEMENT_TYPE
    )
    customer_categories = models.ManyToManyField(
        CustomerCategory, verbose_name="Харилцагчийн төрөл", related_name="promotions",
    )
    customers = models.ManyToManyField(
        Customer, verbose_name="Харилцагчид", related_name="promotions",
    )
    warehouses = models.ManyToManyField(
        Warehouse, verbose_name="Агуулах", related_name="promotions",
    )
    is_implement = models.BooleanField(
        verbose_name="Хэрэгжүүлнэ/Хэрэгжүүлэхгүй", default=True
    )
    ############################################################
    is_active = models.BooleanField(verbose_name="Идэвхитэй", default=True)
    created_at = models.DateTimeField(verbose_name="Үүссэн огноо", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Зассан огноо", auto_now=True)

    class Meta:
        verbose_name = "Урамшуулал"
        verbose_name_plural = "Урамшуулаллууд"
        ordering = ["order", "-id"]

    def __str__(self):
        return self.name

    def get_promotion_type(self):
        return self.get_promotion_type_display()

    get_promotion_type.short_description = "Урамшууллын төрөл"

    def get_implement_type(self):
        return self.get_implement_type_display()

    get_implement_type.short_description = "Харилцагчид хэрэгжүүлэх төрөл"

    def get_date(self):
        start_date = self.start_date.strftime("%Y-%m-%d")
        end_date = self.end_date.strftime("%Y-%m-%d")
        return "%s - %s" % (start_date, end_date)

    get_date.short_description = "Огноо"

    def get_action(self):
        return """
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
            </div>""".format(
            reverse_lazy("employee-promotion-detail", kwargs={"pk": self.pk}),
            reverse_lazy("employee-promotion-history", kwargs={"pk": self.pk}),
            reverse_lazy("employee-promotion-update", kwargs={"pk": self.pk}),
            reverse_lazy("employee-promotion-delete", kwargs={"pk": self.pk}),
        )


class PromotionProduct(models.Model):
    """
    Урамшуулалд орох бүтээгдэхүүн
    """

    promotion = models.ForeignKey(
        Promotion,
        verbose_name="Урамшуулал",
        on_delete=models.CASCADE,
        related_name="promotion_products",
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Бүтээгдэхүүн",
        on_delete=models.CASCADE,
        related_name="promotion_products",
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Тоо хэмжээ", null=True, validators=[validate_nonzero], default=1
    )
    is_not_bonus = models.BooleanField(verbose_name="Авах/Өгөх", default=True)

    class Meta:
        verbose_name = "Урамшууллын бүтээгдэхүүн"
        verbose_name_plural = "Урамшууллын бүтээгдэхүүнүүд"

    def __str__(self):
        return self.promotion.name
