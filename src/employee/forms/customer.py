# -*- coding=utf-8 -*-

from django import forms


from src.customer.models import CustomerCategory, Customer, CEOInformation
from src.warehouse.models import Warehouse

__all__ = ['CustomerFilterForm', 'CustomerForm']


class CustomerFilterForm(forms.ModelForm):
    """
    CustomerFilterForm
    """
    choices = (
        ('', 'Бүгд'),
        ('0', 'Хандах эрхгүй'),
        ('1', 'Хандах эрхтэй'),
    )
    is_has_user = forms.ChoiceField(choices=choices)

    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(), label='Агуулах')

    class Meta:
        model = Customer
        fields = ['name', 'register_no', 'phone', 'warehouse', 'is_has_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].required = False
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-sm'})


class CustomerForm(forms.ModelForm):
    """
    CustomerForm
    """
    warehouses = forms.ModelMultipleChoiceField(
        queryset=Warehouse.objects.all(), label='Агуулахууд')
    customer_category = forms.ModelChoiceField(
        queryset=CustomerCategory.objects.all(), label='Харилцагчийн төрөл')

    class Meta:
        model = CEOInformation
        fields = ['last_name', 'first_name', 'register', 'email', 'phone']

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['warehouses'].queryset = Warehouse.objects.filter(
            company=company)
