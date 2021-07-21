

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from src.warehouse.models import Warehouse
from src.customer.models import Customer
from src.employee.models import Employee
from src.product.models import Product
from src.core import constant as const


class Order(models.Model):
    packing_list_id = models.IntegerField(null=True)
    customer = models.ForeignKey(
        Customer,
        verbose_name='Харилцагч',
        on_delete=models.CASCADE
    )
    seller = models.ForeignKey(
        Employee,
        verbose_name='Ажилтан',
        on_delete=models.CASCADE
    )
    warehouse = models.ForeignKey(
        Warehouse,
        verbose_name='Агуулах',
        on_delete=models.CASCADE
    )
    status = models.IntegerField(
        verbose_name='Төлөв',
        choices=const.ORDER_STATUS
    )
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
        ordering = ['-updated_at']
        verbose_name = 'Захиалга'
        verbose_name_plural = 'Захиалгууд'

    def __str__(self):
        return self.customer.name

    def get_total_price(self):
        return sum(
            int(product.quantity*product.discounted_price)
            for product in self.order_products.all()
        )
    get_total_price.short_description = 'Нийт дүн'

    def get_status(self):
        return dict(const.ORDER_STATUS)[self.status]
    get_status.short_description = 'Төлөв'

    def get_created_date(self):
        return self.created_at.strftime('%Y-%m-%d %H:%S')
    get_total_price.short_description = 'Огноо'

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
              </div>
            </div>'''.format(
            reverse_lazy('employee-order-detail',
                         kwargs={'pk': self.pk})
        )


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Захиалга',
        on_delete=models.CASCADE,
        related_name='order_products'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Бүтээгдэхүүн',
        on_delete=models.CASCADE,
        related_name='order_products'
    )
    quantity = models.PositiveIntegerField()
    quantity_approved = models.PositiveIntegerField(null=True)
    price = models.FloatField()
    discount = models.CharField(max_length=64)
    discount_package = models.CharField(max_length=64, null=True)
    discounted_price = models.FloatField()
    total = models.FloatField()
    is_bonus = models.BooleanField(default=False)

    class Meta:
        ordering = ['product__name']
        verbose_name = 'Захиалгын бүтээгдэхүүн'
        verbose_name_plural = 'Захиалгын бүтээгдэхүүнүүд'

    def __str__(self):
        return self.product.name
