# -*- coding:utf-8 -*-

"""
Сурталчилгаа форм
"""

from django import forms

from src.customer.models import Customer
from src.advertisement.models import Advertisement
from src.employee.forms.widgets import (
    DateRangeInput, AutocompleteSelectMultiple)


__all__ = ['AdvertisementFilterForm', 'AdvertisementInformationForm',
           'AdvertisementImplementTypeForm', 'AdvertisementCustomerCategoryForm',
           'AdvertisementCustomerCategoryForm', 'AdvertisementCustomerForm',
           'AdvertisementWarehouseForm']


class AdvertisementFilterForm(forms.ModelForm):
    """
    Сурталчилгаа филтер форм
    """
    # name = forms.CharField()
    # description = forms.CharField()
    dates = forms.CharField(widget=DateRangeInput())

    class Meta:
        model = Advertisement
        fields = ['name', 'implement_type', 'dates']

    def __init__(self, *args, **kwargs):
        super(AdvertisementFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False
            self.fields[field].widget.attrs.update(
                {'class': 'form-control form-control-sm'})


class AdvertisementInformationForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['name', 'image', 'description']


class AdvertisementImplementTypeForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['implement_type']

    def __init__(self, *args, **kwargs):
        super(AdvertisementImplementTypeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if self.instance and instance.pk:
            self.fields['implement_type'].widget.attrs.update(
                {'readonly': True})

    def clean_implement_type(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.implement_type
        else:
            return self.cleaned_data['implement_type']


class AdvertisementCustomerCategoryForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['customer_categories', 'is_implement']
        widgets = {
            'customer_categories': AutocompleteSelectMultiple('autocomplete-customer-categories')
        }

    # def __init__(self, *args, **kwargs):
    #     super(AdvertisementCustomerCategoryForm,
    #           self).__init__(*args, **kwargs)
    #     self.fields['customer_categories'].queryset = self.fields['customer_categories'].queryset.none()


class AdvertisementCustomerForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['customers', 'is_implement']
        widgets = {
            'customers': AutocompleteSelectMultiple('autocomplete-customers')
        }

    def __init__(self, *args, **kwargs):
        super(AdvertisementCustomerForm, self).__init__(*args, **kwargs)
        self.fields['customers'].queryset = self.fields['customers'].queryset.none()

        if 'CUSTOMER-customers' in self.data:
            try:
                customer_ids = dict(self.data)['CUSTOMER-customers']
                self.fields['customers'].queryset = Customer.objects.filter(
                    id__in=customer_ids)
            except (ValueError, TypeError):
                pass


class AdvertisementWarehouseForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['warehouses', 'is_implement']
        widgets = {
            'warehouses': AutocompleteSelectMultiple('autocomplete-warehouses')
        }

    # def __init__(self, *args, **kwargs):
    #     super(AdvertisementWarehouseForm, self).__init__(*args, **kwargs)
    #     self.fields['warehouses'].queryset = self.fields['warehouses'].queryset.none()
