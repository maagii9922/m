# -*- coding: utf-8 -*-

"""
Харилцагч
"""

from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from src.company.models import Company
from src.warehouse.models import Warehouse


class CustomerCategory(models.Model):
    """
    Харилцагчийн төрөл
    """

    name = models.CharField(verbose_name="Нэр", max_length=64)

    class Meta:
        verbose_name = "Харилцагчийн төрөл"
        verbose_name_plural = "Харилцагчийн төрлүүд"

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    Харилцагчийн мэдээлэл удирдах модель
    """

    customer_category = models.ForeignKey(
        CustomerCategory,
        verbose_name="Харилцагчийн төрөл",
        on_delete=models.CASCADE,
        related_name="customers",
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        verbose_name="Компани",
        on_delete=models.CASCADE,
        related_name="customers",
        null=True,
    )
    parent = models.ForeignKey(
        "Customer",
        verbose_name="Толгой харилцагч",
        on_delete=models.CASCADE,
        related_name="customers",
        null=True,
        blank=True,
    )
    warehouses = models.ManyToManyField(
        Warehouse, verbose_name="Агуулахууд", related_name="customers", blank=True
    )
    user = models.OneToOneField(
        User, verbose_name="Хэрэглэгч", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(verbose_name="Нэр", max_length=256)
    register_no = models.CharField(
        verbose_name="Байгууллагын регистерийн дугаар",
        max_length=32,
        null=True,
        blank=True,
    )
    phone = models.CharField(verbose_name="Утас", max_length=512, null=True, blank=True)
    email = models.EmailField(verbose_name="Имэйл", null=True, blank=True)
    fax = models.CharField(verbose_name="Факс", max_length=512, null=True, blank=True)
    addr_country = models.CharField(
        verbose_name="Улс", max_length=512, null=True, blank=True
    )
    addr_city = models.CharField(
        verbose_name="Аймаг/Хот", max_length=512, null=True, blank=True
    )
    addr_district = models.CharField(
        verbose_name="Сум/Дүүрэг", max_length=512, null=True, blank=True
    )
    addr_street = models.CharField(
        verbose_name="Гудамж 1", max_length=512, null=True, blank=True
    )
    addr_street2 = models.CharField(
        verbose_name="Гудамж 2", max_length=512, null=True, blank=True
    )
    longitude = models.DecimalField(
        verbose_name="Уртраг", max_digits=12, decimal_places=9, null=True, blank=True
    )
    latitude = models.DecimalField(
        verbose_name="Өргөрөг", max_digits=12, decimal_places=9, null=True, blank=True
    )
    is_supplier = models.BooleanField(verbose_name="Нийлүүлэгч эсэх", default=False)
    is_customer = models.BooleanField(verbose_name="Харилцагч эсэх", default=False)
    is_factory = models.BooleanField(verbose_name="Үйлдвэрлэгч эсэх", default=False)
    flag = models.IntegerField(verbose_name="Флаг")
    is_active = models.BooleanField(verbose_name="Идэвхитэй", default=True)
    created_at = models.DateTimeField(verbose_name="Үүссэн огноо", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Зассан огноо", auto_now=True)

    class Meta:
        ordering = ["-updated_at", "id"]
        verbose_name = "Харилцагч"
        verbose_name_plural = "Харилцагчид"

    def __str__(self):
        return self.name

    def get_warehouses(self):
        return " ,\n".join(self.warehouses.all().values_list("name", flat=True))

    get_warehouses.short_description = "Агуулахууд"

    def get_permission(self):
        """
        Хандах эрх
        """
        if getattr(self, "user") is not None and getattr(self, "user").is_active:
            return '<span class="badge badge-success">Хандах эрхтэй</span>'
        elif getattr(self, "user") is not None and not getattr(self, "user").is_active:
            return '<span class="badge badge-danger">Хандах эрх цуцлагдсан</span>'
        return '<span class="badge badge-warning">Хандах эрхгүй</span>'

    get_permission.short_description = "Хандах эрх"

    def get_action(self):
        """
        Үйлдэл
        """
        update = reverse_lazy("employee-customer-update", kwargs={"pk": self.pk})
        active = reverse_lazy("employee-customer-active", kwargs={"pk": self.pk})
        deactive = reverse_lazy("employee-customer-delete", kwargs={"pk": self.pk})

        if self.user:
            config = reverse_lazy(
                "employee-customer-user-update", kwargs={"pk": self.pk}
            )

            if self.user.is_active:

                return """<div class = "dropdown">
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
                        <a class="dropdown-item" href="{0}">Хандах эрх</a>
                        <a class="dropdown-item" href="javascript:;" data-toggle="deleteAlert" data-href="{1}">Хандах эрх цуцлах</a>
                        <a class="dropdown-item" href="{2}">Засах</a>
                    </div>
                    </div>""".format(
                    config, deactive, update
                )

            else:
                return """<div class = "dropdown">
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
                        <a class="dropdown-item" href="{0}">Хандах эрх</a>
                        <a class="dropdown-item" href="javascript:;" data-toggle="deleteAlert" data-href="{1}">Хандах эрх сэргээх</a>
                        <a class="dropdown-item" href="{2}">Засах</a>
                    </div>
                    </div>""".format(
                    config, active, update
                )

        else:
            config = reverse_lazy(
                "employee-customer-user-create", kwargs={"pk": self.pk}
            )

            return """<div class = "dropdown">
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
                    <a class="dropdown-item" href="{0}">Хандах эрх</a>
                    <a class="dropdown-item" href="{1}">Засах</a>
                </div>
                </div>""".format(
                config, update
            )


class CEOInformation(models.Model):
    """
    CEOInformation
    """

    customer = models.OneToOneField(
        Customer,
        verbose_name="Харилцагч",
        on_delete=models.CASCADE,
        related_name="ceo_informations",
    )
    last_name = models.CharField(
        verbose_name="Холбогдох ажилтан овог", max_length=64, null=True, blank=True
    )
    first_name = models.CharField(
        verbose_name="Холбогдох ажилтан нэр", max_length=64, null=True, blank=True
    )
    register = models.CharField(
        verbose_name="Холбогдох ажилтан регистер", max_length=64, null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Холбогдох ажилтан имэйл", null=True, blank=True
    )
    phone = models.CharField(
        verbose_name="Холбогдох ажилтан утас", max_length=64, null=True, blank=True
    )
    is_active = models.BooleanField(verbose_name="Идэвхитэй", default=True)
    created_at = models.DateTimeField(verbose_name="Үүссэн огноо", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Зассан огноо", auto_now=True)

    class Meta:
        ordering = ["-updated_at", "id"]
        verbose_name = "Удирдаж ажилтан"
        verbose_name_plural = "Удирдаж ажилтнууд"

    def __str__(self):
        return self.customer.name
