# -*- coding:utf-8 -*-

"""
Employee CRUD Views
"""

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from src.warehouse.models import Warehouse
from src.employee.models import Employee
from src.employee.forms import (
    EmployeeCreateForm, EmployeeUpdateForm, EmployeeFilterForm)

from . import core as c


__all__ = ['List', 'Create', 'Update', 'Delete',
           'UserCreate', 'UserUpdate', 'load_warehouses']


class List(c.ListView):
    """
    ListView
    """
    queryset = Employee.objects.filter(is_active=True)
    template_name = 'employee/core/list.html'
    page_title = 'Ажилтан'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Ажилтан', ''),
    ]
    add_url = reverse_lazy('employee-create')
    filter_form = EmployeeFilterForm
    fields = ['get_username', 'get_full_name', 'email', 'get_position']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('username', None):
            queryset = queryset.filter(
                user__username__icontains=self.request.GET.get('username'))
        if self.request.GET.get('name', None):
            queryset = queryset.filter(
                Q(user__last_name__icontains=self.request.GET.get('name')) |
                Q(user__first_name__icontains=self.request.GET.get('name'))
            )
        if self.request.GET.get('email', None):
            queryset = queryset.filter(
                user__email__icontains=self.request.GET.get('email'))
        if self.request.GET.get('is_admin') == '0':
            queryset = queryset.filter(is_super_manager=True)
        elif self.request.GET.get('is_admin') == '1':
            queryset = queryset.filter(is_super_manager=False)
        return queryset


class Create(c.CreateView):
    """
    CreateView
    """

    form_class = EmployeeCreateForm
    template_name = 'employee/employee/edit.html'
    success_url = reverse_lazy('employee-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ажилтан нэмэх'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Ажилтан', reverse_lazy('employee-list')),
            ('Ажилтан нэмэх', ''),
        ]
        return context


class Update(c.UpdateView):
    """
    UpdateView
    """
    model = Employee
    form_class = EmployeeUpdateForm
    template_name = 'employee/employee/edit.html'
    success_url = reverse_lazy('employee-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ажилтан засах'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Ажилтан', reverse_lazy('employee-list')),
            ('Ажилтан засах', ''),
        ]
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.object.user.username if self.object.user else ''
        return initial


class Delete(c.RedirectView):
    """
    Delete
    """
    url = reverse_lazy('employee-list')

    def get_redirect_url(self, *args, **kwargs):
        manager = get_object_or_404(Employee, pk=self.kwargs['pk'])
        manager.is_active = False
        manager.save()
        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа')
        return super().get_redirect_url(*args, **kwargs)


class UserCreate(c.CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'employee/employee/edit.html'
    success_url = reverse_lazy('employee-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Нэвтрэх нэр нууц үг'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Ажилтан', reverse_lazy('employee-list')),
            ('Нэвтрэх нэр нууц үг', ''),
        ]
        return context

    def form_valid(self, form):
        user = form.save()
        employee = get_object_or_404(Employee, pk=self.kwargs['employee_pk'])
        employee.user = user
        employee.save()
        return super(UserCreate, self).form_valid(form)


class UserUpdate(c.UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = 'employee/employee/edit.html'
    success_url = reverse_lazy('employee-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Нэвтрэх нэр нууц үг'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Ажилтан', reverse_lazy('employee-list')),
            ('Нэвтрэх нэр нууц үг', ''),
        ]
        return context


def load_warehouses(request):
    """
    form filter
    """
    company_id = request.GET.get('company_id')
    warehouses = Warehouse.objects.filter(company__id=company_id)
    return render(request, 'employee/employee/ajax/warehouses.html', {'warehouses': warehouses})
