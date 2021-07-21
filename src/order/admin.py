from django.contrib import admin
from .models import Order, OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'warehouse', 'status', 'updated_at')


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass
