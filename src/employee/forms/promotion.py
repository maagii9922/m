# -*- coding:utf-8 -*-

"""
Урамшуулал
"""

from django import forms

from src.customer.models import Customer
from src.promotion.models import Product
from src.promotion.models import Promotion, PromotionProduct
from src.employee.forms.widgets import (
    DateRangeInput, AutocompleteSelect, AutocompleteSelectMultiple)


class PromotionFilterForm(forms.ModelForm):
    """
    Урамшуулал шүүлтүүр
    """
    dates = forms.CharField(widget=DateRangeInput())

    class Meta:
        model = Promotion
        fields = ['name', 'promotion_type', 'implement_type', 'dates']

    def __init__(self, *args, **kwargs):
        super(PromotionFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].widget.attrs.update(
                {'class': 'form-control form-control-sm'})


class PromotionInformationForm(forms.ModelForm):
    dates = forms.CharField(label='Огноо', widget=DateRangeInput())

    class Meta:
        model = Promotion
        fields = ['name', 'dates', 'order', 'description']


class PromotionTypeForm(forms.ModelForm):

    class Meta:
        model = Promotion
        fields = ['promotion_type']

    def __init__(self, *args, **kwargs):
        super(PromotionTypeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if self.instance and instance.pk:
            self.fields['promotion_type'].widget.attrs.update(
                {'readonly': True})

    def clean_promotion_type(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.promotion_type
        else:
            return self.cleaned_data['promotion_type']


class PromotionTypeProductForm(forms.ModelForm):
    above_the_number_percent = forms.FloatField(
        label='Тооноос дээш хувь', required=False, min_value=0.1)

    class Meta:
        model = Promotion
        fields = ['product_type', 'products', 'above_the_price', 'promotion_implement_type',
                  'percent', 'price', 'above_the_number']
        widgets = {
            'products': AutocompleteSelectMultiple('autocomplete-products')
        }

    def __init__(self, *args, **kwargs):
        super(PromotionTypeProductForm, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = self.fields['products'].queryset.none()
        self.fields['percent'].widget.attrs.update({'readonly': True})
        self.fields['price'].widget.attrs.update({'readonly': True})
        self.fields['above_the_number'].widget.attrs.update({'readonly': True})
        self.fields['above_the_number_percent'].widget.attrs.update(
            {'readonly': True})

        if self.instance.pk:
            self.fields['products'].queryset = self.instance.products.all()

        if 'promotion_type_product-products' in self.data:
            try:
                product_ids = dict(self.data)[
                    'promotion_type_product-products']
                self.fields['products'].queryset = Product.objects.filter(
                    id__in=product_ids)
            except (ValueError, TypeError):
                pass

    def clean_percent(self):
        percent = self.cleaned_data.get('percent')
        if percent and percent >= 100:
            raise forms.ValidationError("100%-с бага дүн оруулна уу")
        return percent

    def clean_above_the_number_percent(self):
        above_the_number_percent = self.cleaned_data.get(
            'above_the_number_percent')
        if above_the_number_percent and above_the_number_percent >= 100:
            raise forms.ValidationError("100%-с бага дүн оруулна уу")
        return above_the_number_percent


class PromotionTypePackageForm(forms.ModelForm):

    class Meta:
        model = Promotion
        fields = ['quantity', 'percent']

    def __init__(self, *args, **kwargs):
        super(PromotionTypePackageForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].required = False
        self.fields['percent'].required = True

    def clean_percent(self):
        percent = self.cleaned_data.get('percent')
        if percent and percent >= 100:
            raise forms.ValidationError("100%-с бага дүн оруулна уу")
        return percent


class PromotionTypeSupplierForm(forms.ModelForm):
    above_the_number_percent = forms.FloatField(
        label='Тооноос дээш хувь', required=False)

    class Meta:
        model = Promotion
        fields = ['supplier', 'product_type', 'products', 'above_the_price',
                  'promotion_implement_type', 'percent', 'price', 'above_the_number',
                  'above_the_number_percent']
        widgets = {
            'supplier': AutocompleteSelect('autocomplete-suppliers'),
            # 'products': AutocompleteSelectMultiple('autocomplete-products')
        }

    def __init__(self, *args, **kwargs):
        super(PromotionTypeSupplierForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = self.fields['supplier'].queryset.filter(
            seller_products__isnull=False).none()
        self.fields['products'].queryset = self.fields['products'].queryset.none()
        self.fields['percent'].widget.attrs.update({'readonly': True})
        self.fields['price'].widget.attrs.update({'readonly': True})
        self.fields['above_the_number'].widget.attrs.update({'readonly': True})
        self.fields['above_the_number_percent'].widget.attrs.update(
            {'readonly': True})

        if self.instance.pk:
            if self.instance.supplier:
                self.fields['supplier'].queryset = Customer.objects.filter(
                    id=self.instance.supplier.id)
                self.fields['products'].queryset = self.instance.products.all()

        if 'promotion_type_supplier-supplier' in self.data:
            try:
                supplier_id = self.data.get('promotion_type_supplier-supplier')
                self.fields['supplier'].queryset = Customer.objects.filter(
                    id=supplier_id)
            except (ValueError, TypeError):
                pass

        if 'promotion_type_supplier-products' in self.data:
            try:
                product_ids = dict(self.data).get(
                    'promotion_type_supplier-products')
                self.fields['products'].queryset = Product.objects.filter(
                    id__in=product_ids)
            except (ValueError, TypeError):
                pass

    def clean_percent(self):
        percent = self.cleaned_data.get('percent')
        if percent and percent >= 100:
            raise forms.ValidationError("100%-с бага дүн оруулна уу")
        return percent

    def clean_above_the_number_percent(self):
        above_the_number_percent = self.cleaned_data.get(
            'above_the_number_percent')
        if above_the_number_percent and above_the_number_percent >= 100:
            raise forms.ValidationError("100%-с бага дүн оруулна уу")
        return above_the_number_percent


class PromotionTypeAccForm(forms.Form):
    pass


class ImplementTypeForm(forms.ModelForm):

    class Meta:
        model = Promotion
        fields = ['implement_type']


class ImplementTypeCustomerCategoryForm(forms.ModelForm):

    class Meta:
        model = Promotion
        fields = ['customer_categories', 'is_implement']
        widgets = {
            'customer_categories': AutocompleteSelectMultiple('autocomplete-customer-categories')
        }


class ImplementTypeCustomerForm(forms.ModelForm):

    class Meta:
        model = Promotion
        fields = ['customers', 'is_implement']
        widgets = {
            'customers': AutocompleteSelectMultiple('autocomplete-customers')
        }

    def __init__(self, *args, **kwargs):
        super(ImplementTypeCustomerForm, self).__init__(*args, **kwargs)
        self.fields['customers'].queryset = self.fields['customers'].queryset.none()

        if 'implement_type_customer-customers' in self.data:
            try:
                customer_ids = dict(self.data)[
                    'implement_type_customer-customers']
                self.fields['customers'].queryset = Customer.objects.filter(
                    id__in=customer_ids)
            except (ValueError, TypeError):
                pass


class ImplementTypeWarehouseForm(forms.ModelForm):

    class Meta:
        model = Promotion
        fields = ['warehouses', 'is_implement']
        widgets = {
            'warehouses': AutocompleteSelectMultiple('autocomplete-warehouses')
        }


class PromotionPackageForm(forms.ModelForm):

    class Meta:
        model = PromotionProduct
        fields = ['product', 'quantity']
        widgets = {
            'product': AutocompleteSelect('autocomplete-products')
        }

    def __init__(self, *args, **kwargs):
        super(PromotionPackageForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = self.fields['product'].queryset.none()
        # self.fields['product'].required = True
        self.fields['quantity'].required = False
        self.fields['quantity'].widget.attrs.update(
            {'class': 'form-control'})

        if self.instance.pk:
            self.fields['product'].queryset = Product.objects.filter(
                id=self.instance.product.id)

        if 'promotion_type_package_formset-TOTAL_FORMS' in self.data:
            total_forms = self.data.get(
                'promotion_type_package_formset-TOTAL_FORMS')
            product_ids = []
            for i in range(0, int(total_forms)):
                key = 'promotion_type_package_formset-{0}-product'.format(i)
                if self.data.get(key):
                    product_ids.append(self.data.get(key))
            self.fields['product'].queryset = Product.objects.filter(
                id__in=product_ids)


class PromotionAccForm(forms.ModelForm):

    class Meta:
        model = PromotionProduct
        fields = ['product', 'quantity', 'is_not_bonus']
        widgets = {
            'product': AutocompleteSelect('autocomplete-products')
        }

    def __init__(self, *args, **kwargs):
        super(PromotionAccForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = self.fields['product'].queryset.none()
        self.fields['quantity'].required = False
        self.fields['quantity'].widget.attrs.update(
            {'class': 'form-control'})

        if self.instance.pk:
            print(self.instance.product)
            self.fields['product'].queryset = Product.objects.filter(
                id=self.instance.product.id)

        if 'promotion_type_acc-TOTAL_FORMS' in self.data:
            total_forms = self.data.get(
                'promotion_type_acc-TOTAL_FORMS')
            product_ids = []
            for i in range(0, int(total_forms)):
                key = 'promotion_type_acc-{0}-product'.format(i)
                if self.data.get(key):
                    product_ids.append(self.data.get(key))
            self.fields['product'].queryset = Product.objects.filter(
                id__in=product_ids)


PromotionPackageFormset = forms.inlineformset_factory(
    Promotion, PromotionProduct, form=PromotionPackageForm, extra=0, min_num=2, max_num=100)


PromotionAccFormset = forms.inlineformset_factory(
    Promotion, PromotionProduct, form=PromotionAccForm, extra=0, min_num=2, max_num=100)
