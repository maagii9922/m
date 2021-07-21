

from django.views.generic import ListView
from django.http import JsonResponse

from src.warehouse.models import Warehouse
from src.customer.models import CustomerCategory, Customer
from src.product.models import Product


class Warehouses(ListView):
    model = Warehouse
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """

        self.term = request.GET.get('term', '')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {'id': str(obj.pk), 'text': str(obj)}
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def get_queryset(self):
        queryset = super(Warehouses, self).get_queryset()
        queryset = queryset.filter(name__icontains=self.term)
        return queryset


class CustomerCategories(ListView):
    model = CustomerCategory
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """

        self.term = request.GET.get('term', '')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {'id': str(obj.pk), 'text': str(obj)}
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def get_queryset(self):
        queryset = super(CustomerCategories, self).get_queryset()
        queryset = queryset.filter(name__icontains=self.term)
        return queryset


class Customers(ListView):
    model = Customer
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """

        self.term = request.GET.get('term', '')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {'id': str(obj.pk), 'text': str(obj)}
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def get_queryset(self):
        queryset = super(Customers, self).get_queryset()
        queryset = queryset.filter(name__icontains=self.term)
        return queryset


class Suppliers(ListView):
    # model = Customer
    queryset = Customer.objects.filter(
        seller_products__isnull=False).distinct()  # Нийлүүлэх бүтээгдэхүүн хоосон биш бол
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """

        self.term = request.GET.get('term', '')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {'id': str(obj.pk), 'text': str(obj)}
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def get_queryset(self):
        queryset = super(Suppliers, self).get_queryset()
        queryset = queryset.filter(name__icontains=self.term)
        return queryset


class Products(ListView):
    model = Product
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """

        self.term = request.GET.get('term', '')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {'id': str(obj.pk), 'text': str(obj)}
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def get_queryset(self):
        queryset = super(Products, self).get_queryset()
        queryset = queryset.filter(name__icontains=self.term)
        return queryset
