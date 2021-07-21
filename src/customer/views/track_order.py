
from django.conf import settings
from django.shortcuts import get_object_or_404

from src.core import constant as const
from src.fetch.connection import Connection
from src.warehouse.models import Warehouse
from src.order.models import Order

from . import core as c


__all__ = ['TrackOrder', 'TrackOrderDetail']


class TrackOrder(c.ListView):
    model = Order
    template_name = 'customer/track/order.html'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        self.warehouse = get_object_or_404(
            Warehouse, pk=request.session[settings.WAREHOUSE_SESSION_ID])
        return super(TrackOrder, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(TrackOrder, self).get_queryset()
        status = self.kwargs.get('status')
        queryset = queryset.filter(
            customer=self.request.user.customer,
            packing_list_id__isnull=False
        )
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TrackOrder, self).get_context_data(**kwargs)
        context['status'] = dict(const.ORDER_STATUS)
        # packing_list_ids = list(
        #     context['object_list'].values_list('packing_list_id', flat=True))
        # connection = Connection.get_instance()
        # result = connection.track_order(
        #     self.warehouse.company.id, packing_list_ids)
        # if result.json().get('status') == 'success':
        #     for item in result.json().get('data'):
        #         order = get_object_or_404(
        #             Order, packing_list_id=item['packing_list_id'])
        #         order.status = item['status']
        #         order.save()
        return context


class TrackOrderDetail(c.DetailView):
    model = Order
    template_name = 'customer/track/order_detail.html'
