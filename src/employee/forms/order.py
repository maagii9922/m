

from django import forms

from src.core.constant import ORDER_STATUS
from src.employee.forms.widgets import DateRangeInput
from src.warehouse.models import Warehouse
from src.order.models import Order


__all__ = ['OrderFilterForm']


ORDER_STATUS_EMPTY = [('', '---------')] + list(ORDER_STATUS)


class OrderFilterForm(forms.Form):
    customer = forms.CharField()
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all())
    status = forms.ChoiceField(choices=ORDER_STATUS_EMPTY)
    total = forms.IntegerField()
    dates = forms.CharField(widget=DateRangeInput())

    def __init__(self, *args, **kwargs):
        super(OrderFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].widget.attrs.update(
                {'class': 'form-control form-control-sm'})
