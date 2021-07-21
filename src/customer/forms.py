# -*- coding: utf-8 -*-

from django import forms

from src.order.models import OrderProduct


class CartQuantityForm(forms.ModelForm):

    class Meta:
        model = OrderProduct
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super(CartQuantityForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({
            'class': 'input-number__input form-control form-control-lg'})
        self.fields['quantity'].initial = 1
