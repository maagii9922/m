# -*- coding:utf-8 -*-

"""
Сурталчилгаа view
"""
import os

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from src.advertisement.models import Advertisement
from src.employee import forms as f
from src.core import constant as const, actions

from . import core as c


__all__ = ['AdvertisementList', 'AdvertisementCreate',
           'AdvertisementUpdate', 'AdvertisementDetail',
           'AdvertisementHistory', 'AdvertisementDelete']


class AdvertisementList(c.ListView):
    """
    Сурталчилгааны жагсаалт харуулах
    """
    queryset = Advertisement.objects.filter(is_active=True)
    page_title = 'Сурталчилгаа'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Сурталчилгаа', ''),
    ]
    add_url = reverse_lazy('employee-advertisement-create')
    filter_form = f.AdvertisementFilterForm
    fields = ['name', 'get_implement_type', 'updated_at']
    actions = [{'name': 'Засах', 'url': 'manager-advertisement-update'}]
    paginate_by = 20

    def get_queryset(self):
        qs = Advertisement.objects.filter(is_active=True)
        if self.request.GET.get('name', None):
            qs = qs.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('implement_type', None):
            qs = qs.filter(
                implement_type=self.request.GET.get('implement_type'))
        if self.request.GET.get('dates'):
            dates = self.request.GET.get('dates').split(" - ")
            qs = qs.filter(updated_at__date__range=dates)
        return qs


FORM = (
    ('INFORMATION', f.AdvertisementInformationForm),
    ('IMPLEMENT_TYPE', f.AdvertisementImplementTypeForm),
    ('CUSTOMER_CATEGORY', f.AdvertisementCustomerCategoryForm),
    ('CUSTOMER', f.AdvertisementCustomerForm),
    ('WAREHOUSE', f.AdvertisementWarehouseForm),
)

TEMPLATES = {
    'INFORMATION': 'employee/advertisement/wizard/information.html',
    'IMPLEMENT_TYPE': 'employee/advertisement/wizard/implement_type.html',
    'CUSTOMER_CATEGORY': 'employee/advertisement/wizard/customer_category.html',
    'CUSTOMER': 'employee/advertisement/wizard/customer.html',
    'WAREHOUSE': 'employee/advertisement/wizard/warehouse.html'
}


def condition_customer_category(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(
        'IMPLEMENT_TYPE') or {'implement_type': 'none'}

    return cleaned_data['implement_type'] == const.IMPLEMENT_TYPE_CUSTOMER_CATEGORY


def condition_customer(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(
        'IMPLEMENT_TYPE') or {'implement_type': 'none'}

    return cleaned_data['implement_type'] == const.IMPLEMENT_TYPE_CUSTOMER


def condition_warehouse(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(
        'IMPLEMENT_TYPE') or {'implement_type': 'none'}

    return cleaned_data['implement_type'] == const.IMPLEMENT_TYPE_WAREHOUSE


class AdvertisementCreate(c.SessionWizardView):
    page_title = 'Сурталчилгаа нэмэх'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Сурталчилгаа', reverse_lazy('employee-advertisement-list')),
        ('Сурталчилгаа нэмэх', ''),
    ]
    form_list = FORM
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    condition_dict = {
        'CUSTOMER_CATEGORY': condition_customer_category,
        'CUSTOMER': condition_customer,
        'WAREHOUSE': condition_warehouse
    }

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        form_data = {key: form.cleaned_data for key, form in form_dict.items()}
        information_form = form_dict['INFORMATION']
        advertisement = information_form.save(commit=False)
        implement_type_data = form_data['IMPLEMENT_TYPE']
        implement_type = implement_type_data['implement_type']
        if implement_type == const.IMPLEMENT_TYPE_ALL:
            advertisement.implement_type = implement_type
            advertisement.save()
        elif implement_type == const.IMPLEMENT_TYPE_CUSTOMER_CATEGORY:
            advertisement.implement_type = implement_type
            advertisement.is_implement = form_data['CUSTOMER_CATEGORY']['is_implement']
            advertisement.save()
            for category in form_data['CUSTOMER_CATEGORY']['customer_categories']:
                advertisement.customer_categories.add(category)
        elif implement_type == const.IMPLEMENT_TYPE_CUSTOMER:
            advertisement.implement_type = implement_type
            advertisement.is_implement = form_data['CUSTOMER']['is_implement']
            advertisement.save()
            for customer in form_data['CUSTOMER']['customers']:
                advertisement.customers.add(customer)
        elif implement_type == const.IMPLEMENT_TYPE_WAREHOUSE:
            advertisement.implement_type = implement_type
            advertisement.is_implement = form_data['WAREHOUSE']['is_implement']
            advertisement.save()
            for warehouse in form_data['WAREHOUSE']['warehouses']:
                advertisement.warehouses.add(warehouse)

        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа.')
        actions.log_create(self.request, advertisement)
        return redirect('employee-advertisement-list')


class AdvertisementUpdate(c.SessionWizardView):
    page_title = 'Сурталчилгаа засах'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Сурталчилгаа', reverse_lazy('employee-advertisement-list')),
        ('Сурталчилгаа засах', ''),
    ]
    form_list = FORM
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    condition_dict = {
        'CUSTOMER_CATEGORY': condition_customer_category,
        'CUSTOMER': condition_customer,
        'WAREHOUSE': condition_warehouse
    }

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_instance(self, step):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            advertisement = get_object_or_404(Advertisement, pk=pk)
            return advertisement
        return self.instance_dict.get(step, None)

    def done(self, form_list, form_dict, **kwargs):
        form_data = {key: form.cleaned_data for key, form in form_dict.items()}
        information_form = form_dict['INFORMATION']
        advertisement = information_form.save(commit=False)
        implement_type_data = form_data['IMPLEMENT_TYPE']
        implement_type = implement_type_data['implement_type']
        if implement_type == const.IMPLEMENT_TYPE_ALL:
            advertisement.implement_type = implement_type
            advertisement.save()
        elif implement_type == const.IMPLEMENT_TYPE_CUSTOMER_CATEGORY:
            advertisement.implement_type = implement_type
            advertisement.is_implement = form_data['CUSTOMER_CATEGORY']['is_implement']
            advertisement.save()
            advertisement.customer_categories.clear()
            for category in form_data['CUSTOMER_CATEGORY']['customer_categories']:
                advertisement.customer_categories.add(category)
        elif implement_type == const.IMPLEMENT_TYPE_CUSTOMER:
            advertisement.implement_type = implement_type
            advertisement.is_implement = form_data['CUSTOMER']['is_implement']
            advertisement.save()
            advertisement.customers.clear()
            for customer in form_data['CUSTOMER']['customers']:
                advertisement.customers.add(customer)
        elif implement_type == const.IMPLEMENT_TYPE_WAREHOUSE:
            advertisement.implement_type = implement_type
            advertisement.is_implement = form_data['WAREHOUSE']['is_implement']
            advertisement.save()
            advertisement.warehouses.clear()
            for warehouse in form_data['WAREHOUSE']['warehouses']:
                advertisement.warehouses.add(warehouse)

        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа.')
        actions.log_update(self.request, advertisement)
        return redirect('employee-advertisement-list')


class AdvertisementDetail(c.DetailView):
    model = Advertisement
    template_name = 'employee/advertisement/detail.html'


class AdvertisementHistory(c.DetailView):
    model = Advertisement
    template_name = 'employee/core/history.html'

    def get_context_data(self, **kwargs):
        context = super(AdvertisementHistory, self).get_context_data(**kwargs)
        obj = self.object
        context['action_list'] = LogEntry.objects.filter(
            content_type_id=ContentType.objects.get_for_model(obj).pk, object_id=obj.pk)
        return context


class AdvertisementDelete(c.RedirectView):
    url = reverse_lazy('employee-advertisement-list')

    def get_redirect_url(self, *args, **kwargs):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        advertisement.is_active = False
        advertisement.save()
        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа')
        actions.log_delete(self.request, advertisement)
        return super().get_redirect_url(*args, **kwargs)
