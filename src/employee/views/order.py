# -*- coding:utf-8 -*-

from django.urls import reverse_lazy

from src.order.models import Order
from src.employee.views import core as c
from src.employee import forms as f

__all__ = ['Orders', 'OrderDetail']


class Orders(c.ListView):
    model = Order
    page_title = 'Захиалга'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Захиалга', ''),
    ]
    fields = ['customer', 'warehouse', 'get_status',
              'get_total_price', 'get_created_date']
    filter_form = f.OrderFilterForm
    paginate_by = 20

    def get_queryset(self):
        queryset = super(Orders, self).get_queryset()
        if self.request.GET.get('customer'):
            queryset = queryset.filter(
                customer__name__icontains=self.request.GET.get('customer'))
        if self.request.GET.get('warehouse'):
            queryset = queryset.filter(
                warehouse__id=self.request.GET.get('warehouse'))
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET.get('status'))
        if self.request.GET.get('dates'):
            start = self.request.GET.get('dates').split(' - ')[0] + ' 00:00:00'
            end = self.request.GET.get('dates').split(' - ')[1] + ' 23:59:59'
            queryset = queryset.filter(created_at__range=[start, end])
        return queryset


class OrderDetail(c.DetailView):
    model = Order
    template_name = 'employee/order/detail.html'
