# -*- coding:utf-8 -*-

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from src.customer.models import Customer
from src.employee.forms import CustomerFilterForm, CustomerForm
# from src.warehouse.models import Warehouse

from . import core as c


__all__ = ['CustomerList', 'CustomerUserCreate', 'CustomerUserUpdate',
           'CustomerUpdate', 'CustomerActive', 'CustomerDelete']


class CustomerList(c.ListView):
    """
    CustomerList
    """
    queryset = Customer.objects.filter(is_active=True, company__isnull=False)
    page_title = 'Харилцагч'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Харилцагч', ''),
    ]
    filter_form = CustomerFilterForm
    fields = ['name', 'register_no', 'phone',
              'get_warehouses', 'get_permission']
    paginate_by = 20

    def get_queryset(self):
        queryset = super(CustomerList, self).get_queryset()

        name = self.request.GET.get('name')
        register_no = self.request.GET.get('register_no')
        phone = self.request.GET.get('phone')
        warehouse = self.request.GET.get('warehouse')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if register_no:
            queryset = queryset.filter(register_no__icontains=register_no)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        if warehouse:
            queryset = queryset.filter(warehouses=warehouse)
        if self.request.GET.get('is_has_user') == '1':
            queryset = queryset.filter(user__isnull=False)
        elif self.request.GET.get('is_has_user') == '0':
            queryset = queryset.filter(user__isnull=True)

        # Хэрэв менежер компани хариуцдаг бол тухайн компаний харилцагч сонгоно
        if not self.request.user.employee.is_super_manager:
            queryset = queryset.filter(
                company=self.request.user.employee.company,
                # warehouses__in=self.request.user.employee.warehouses.all()
            )
        return queryset


class CustomerUserCreate(c.CreateView):
    """
    Customer user create class based view
    """
    form_class = UserCreationForm
    template_name = 'employee/core/edit.html'
    success_url = reverse_lazy('employee-customer-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Харилцагчийн хандах эрхийн тохиргоо'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Харилцагч', reverse_lazy('employee-customer-list')),
            ('Харилцагчийн хандах эрхийн тохиргоо', ''),
        ]
        return context

    def get_initial(self):
        initial = super(CustomerUserCreate, self).get_initial()
        customer = get_object_or_404(Customer, pk=self.kwargs.get('pk'))
        initial['username'] = customer.register_no
        return initial

    def form_valid(self, form):
        user = form.save()
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'])
        customer.user = user
        customer.save()
        return super().form_valid(form)


class CustomerUserUpdate(c.UpdateView):
    """
    Customer user update class based view
    """
    form_class = UserCreationForm
    template_name = 'employee/core/edit.html'
    success_url = reverse_lazy('employee-customer-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Харилцагчийн хандах эрхийн тохиргоо'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Харилцагч', reverse_lazy('employee-customer-list')),
            ('Харилцагчийн хандах эрхийн тохиргоо', ''),
        ]
        return context

    def get_object(self):
        obj = get_object_or_404(Customer, pk=self.kwargs['pk'])
        return obj.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs['readonly'] = True
        return form


class CustomerUpdate(c.FormView):
    """
    CustomerUpdate
    """
    form_class = CustomerForm
    template_name = 'employee/core/edit.html'
    success_url = reverse_lazy('employee-customer-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Харилцагчийн тохиргоо'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Харилцагч', reverse_lazy('employee-customer-list')),
            ('Харилцагчийн тохиргоо', ''),
        ]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'])
        kwargs.update({'company': customer.company})
        if hasattr(customer, 'ceo_informations'):
            kwargs.update({'instance': customer.ceo_informations})
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'])
        initial['warehouses'] = customer.warehouses.all()
        initial['customer_category'] = customer.customer_category
        return initial

    def form_valid(self, form):
        obj = form.save(commit=False)
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'])
        customer_category = form.cleaned_data['customer_category']
        customer.customer_category = customer_category
        customer.save()
        customer.warehouses.clear()
        for warehouse in form.cleaned_data['warehouses']:
            customer.warehouses.add(warehouse)
        if not hasattr(obj, 'customer'):
            obj.customer = customer
        obj.save()
        return super().form_valid(form)


class CustomerActive(c.RedirectView):
    """
    DeleteView
    """
    url = reverse_lazy('employee-customer-list')

    def get_redirect_url(self, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'])
        if customer.user:
            user = customer.user
            user.is_active = True
            user.save()
        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа')
        return super().get_redirect_url(*args, **kwargs)


class CustomerDelete(c.RedirectView):
    """
    DeleteView
    """
    url = reverse_lazy('employee-customer-list')

    def get_redirect_url(self, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'])
        if customer.user:
            user = customer.user
            user.is_active = False
            user.save()
        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа')
        return super().get_redirect_url(*args, **kwargs)
