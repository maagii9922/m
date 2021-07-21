# -*- coding:utf-8 -*-

"""
Promotion views
"""

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.shortcuts import redirect, get_object_or_404, render

from src.core import constant as const, actions
from src.product.models import Product
from src.promotion.models import Promotion, PromotionProduct
from src.employee.forms import promotion as pf
from src.employee.views import core as c


__all__ = ['PromotionList', 'PromotionCreate', 'PromotionUpdate',
           'PromotionDetail', 'PromotionHistory', 'PromotionDelete', 'load_products']


class PromotionList(c.ListView):
    """
    Урамшуулал жагсаалт
    """
    queryset = Promotion.objects.filter(is_active=True)
    page_title = 'Урамшуулал'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Урамшуулал', ''),
    ]
    add_url = reverse_lazy('employee-promotion-create')
    filter_form = pf.PromotionFilterForm
    fields = ['name', 'get_promotion_type', 'get_implement_type', 'get_date']
    paginate_by = 20

    def get_queryset(self):
        queryset = super(PromotionList, self).get_queryset()
        if not hasattr(self.request.user.employee, 'is_super_manager'):
            pass
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        promotion_type = self.request.GET.get('promotion_type')
        if promotion_type:
            queryset = queryset.filter(promotion_type=promotion_type)

        implement_type = self.request.GET.get('implement_type')
        if implement_type:
            queryset = queryset.filter(implement_type=implement_type)

        dates = self.request.GET.get('dates')
        if dates:
            start_date = dates.split(' - ')[0] + ' 00:00:00'
            end_date = dates.split(' - ')[1] + ' 23:59:59'
            queryset = queryset.filter(end_date__range=[start_date, end_date])

        return queryset


FORMS = [
    ('promotion_information', pf.PromotionInformationForm),
    ('promotion_type', pf.PromotionTypeForm),
    ('promotion_type_product', pf.PromotionTypeProductForm),
    ('promotion_type_package_formset', pf.PromotionPackageFormset),
    ('promotion_type_package', pf.PromotionTypePackageForm),
    ('promotion_type_supplier', pf.PromotionTypeSupplierForm),
    ('promotion_type_acc', pf.PromotionAccFormset),
    ('implement_type', pf.ImplementTypeForm),
    ('implement_type_customer_category', pf.ImplementTypeCustomerCategoryForm),
    ('implement_type_customer', pf.ImplementTypeCustomerForm),
    ('implement_type_warehouse', pf.ImplementTypeWarehouseForm),
]

TEMPLATES = {
    'promotion_information': 'employee/promotion/wizard/promotion/information.html',
    'promotion_type': 'employee/promotion/wizard/promotion/type.html',
    'promotion_type_product': 'employee/promotion/wizard/promotion/type_product.html',
    'promotion_type_package_formset': 'employee/promotion/wizard/promotion/type_package_formset.html',
    'promotion_type_package': 'employee/promotion/wizard/promotion/type_package.html',
    'promotion_type_supplier': 'employee/promotion/wizard/promotion/type_supplier.html',
    'promotion_type_acc': 'employee/promotion/wizard/promotion/type_acc.html',
    'implement_type': 'employee/promotion/wizard/implement/type.html',
    'implement_type_customer_category': 'employee/promotion/wizard/implement/type_customer_category.html',
    'implement_type_customer': 'employee/promotion/wizard/implement/type_customer.html',
    'implement_type_warehouse': 'employee/promotion/wizard/implement/type_warehouse.html'
}


def promotion_type_product(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('promotion_type') or {
        'promotion_type': 'none'}

    return cleaned_data['promotion_type'] == const.PROMOTION_TYPE_PRODUCT


def promotion_type_package(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('promotion_type') or {
        'promotion_type': 'none'}
    return cleaned_data['promotion_type'] == const.PROMOTION_TYPE_PACKAGE


def promotion_type_supplier(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('promotion_type') or {
        'promotion_type': 'none'}
    return cleaned_data['promotion_type'] == const.PROMOTION_TYPE_SUPPLIER


def promotion_type_acc(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('promotion_type') or {
        'promotion_type': 'none'}
    return cleaned_data['promotion_type'] == const.PROMOTION_TYPE_ACC


def implement_type_customer_category(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('implement_type') or {
        'implement_type': 'none'}
    return cleaned_data['implement_type'] == const.IMPLEMENT_TYPE_CUSTOMER_CATEGORY


def implement_type_customer(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('implement_type') or {
        'implement_type': 'none'}
    return cleaned_data['implement_type'] == const.IMPLEMENT_TYPE_CUSTOMER


def implement_type_warehouse(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('implement_type') or {
        'implement_type': 'none'}
    return cleaned_data['implement_type'] == const.IMPLEMENT_TYPE_WAREHOUSE


class PromotionCreate(c.SessionWizardView):
    page_title = 'Урамшуулал нэмэх'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Урамшуулал', reverse_lazy('employee-promotion-list')),
        ('Урамшуулал нэмэх', ''),
    ]
    form_list = FORMS
    condition_dict = {
        'promotion_type_product': promotion_type_product,
        'promotion_type_package_formset': promotion_type_package,
        'promotion_type_package': promotion_type_package,
        'promotion_type_supplier': promotion_type_supplier,
        'promotion_type_acc': promotion_type_acc,
        'implement_type_customer_category': implement_type_customer_category,
        'implement_type_customer': implement_type_customer,
        'implement_type_warehouse': implement_type_warehouse
    }

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        form_data = {key: form.cleaned_data
                     for key, form in form_dict.items()}

        promotion_information_form = form_dict['promotion_information']
        promotion = promotion_information_form.save(commit=False)
        start_date = promotion_information_form.cleaned_data['dates'].split(
            ' - ')[0]
        end_date = promotion_information_form.cleaned_data['dates'].split(
            ' - ')[1] + ' 23:59:59'
        promotion.start_date = start_date
        promotion.end_date = end_date

        implement_type = form_data['implement_type']['implement_type']
        promotion.implement_type = implement_type

        promotion_type = form_data['promotion_type']['promotion_type']
        promotion.promotion_type = promotion_type

        if promotion_type == const.PROMOTION_TYPE_PRODUCT:
            data = form_data['promotion_type_product']
            promotion.product_type = data['product_type']
            promotion.promotion_implement_type = data['promotion_implement_type']
            promotion.above_the_price = data['above_the_price']
            promotion.percent = data['percent']
            promotion.price = data['price']
            promotion.above_the_number = data['above_the_number']
            if data['promotion_implement_type'] == \
                    const.PROMOTION_IMPLEMENT_TYPE_ABOVE_THE_NUMBER:
                promotion.percent = data['above_the_number_percent']
            promotion.save()
            for product in form_data['promotion_type_product']['products']:
                promotion.products.add(product)

        elif promotion_type == const.PROMOTION_TYPE_PACKAGE:
            data = form_data['promotion_type_package']
            promotion.promotion_implement_type = const.PROMOTION_IMPLEMENT_TYPE_PERCENT
            promotion.quantity = data['quantity']
            promotion.percent = data['percent']
            promotion.save()
            products = form_data['promotion_type_package_formset']
            for product in products:
                if not product['quantity']:
                    quantity = 0
                else:
                    quantity = product['quantity']
                PromotionProduct.objects.create(
                    promotion=promotion,
                    product=product['product'],
                    quantity=quantity
                )

        elif promotion_type == const.PROMOTION_TYPE_SUPPLIER:
            data = form_data['promotion_type_supplier']
            promotion.supplier = data['supplier']
            promotion.product_type = data['product_type']
            promotion.above_the_price = data['above_the_price']
            promotion.promotion_implement_type = data['promotion_implement_type']
            promotion.percent = data['percent']
            promotion.price = data['price']
            promotion.above_the_number = data['above_the_number']
            if data['promotion_implement_type'] == \
                    const.PROMOTION_IMPLEMENT_TYPE_ABOVE_THE_NUMBER:
                promotion.percent = data['above_the_number_percent']
            promotion.save()
            for product in data['products']:
                promotion.products.add(product)

        elif promotion_type == const.PROMOTION_TYPE_ACC:
            promotion.save()
            for product in form_data['promotion_type_acc']:
                PromotionProduct.objects.create(
                    promotion=promotion,
                    product=product['product'],
                    quantity=product['quantity'],
                    is_not_bonus=product['is_not_bonus']
                )

        if implement_type == const.IMPLEMENT_TYPE_CUSTOMER_CATEGORY:
            idata = form_data['implement_type_customer_category']
            for customer_category in idata['customer_categories']:
                promotion.customer_categories.add(customer_category)
                promotion.is_implement = idata['is_implement']
                promotion.save()

        elif implement_type == const.IMPLEMENT_TYPE_CUSTOMER:
            idata = form_data['implement_type_customer']
            for customer in idata['customers']:
                promotion.customers.add(customer)
                promotion.is_implement = idata['is_implement']
                promotion.save()

        elif implement_type == const.IMPLEMENT_TYPE_WAREHOUSE:
            idata = form_data['implement_type_warehouse']
            for warehouse in idata['warehouses']:
                promotion.warehouses.add(warehouse)
                promotion.is_implement = idata['is_implement']
                promotion.save()

        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа.')
        actions.log_create(self.request, promotion)
        return redirect('employee-promotion-list')


class PromotionUpdate(c.SessionWizardView):
    page_title = 'Урамшуулал засах'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Урамшуулал', reverse_lazy('employee-promotion-list')),
        ('Урамшуулал засах', ''),
    ]
    form_list = FORMS
    template_name = 'employee/promotion/edit.html'
    condition_dict = {
        'promotion_type_product': promotion_type_product,
        'promotion_type_package_formset': promotion_type_package,
        'promotion_type_package': promotion_type_package,
        'promotion_type_supplier': promotion_type_supplier,
        'promotion_type_acc': promotion_type_acc,
        'promotion_type_acc_give': promotion_type_acc,
        "implement_type_customer_category": implement_type_customer_category,
        "implement_type_customer": implement_type_customer,
        "implement_type_warehouse": implement_type_warehouse
    }

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_instance(self, step):
        if 'pk' in self.kwargs:
            promotion_id = self.kwargs['pk']
            promotion = Promotion.objects.get(id=promotion_id)
            return promotion
        return self.instance_dict.get(step, None)

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if step == 'promotion_information':
            if 'pk' in self.kwargs:
                promotion_id = self.kwargs['pk']
                promotion = Promotion.objects.get(id=promotion_id)
                dates = '{0} - {1}'.format(promotion.start_date.date(),
                                           promotion.end_date.date())
                initial.update({'dates': dates})
        return initial

    def done(self, form_list, form_dict, **kwargs):
        form_data = {key: form.cleaned_data
                     for key, form in form_dict.items()}

        promotion_information_form = form_dict['promotion_information']
        promotion = promotion_information_form.save(commit=False)
        start_date = promotion_information_form.cleaned_data['dates'].split(
            ' - ')[0]
        end_date = promotion_information_form.cleaned_data['dates'].split(
            ' - ')[1] + ' 23:59:59'
        promotion.start_date = start_date
        promotion.end_date = end_date

        implement_type = form_data['implement_type']['implement_type']
        promotion.implement_type = implement_type

        promotion_type = form_data['promotion_type']['promotion_type']
        promotion.promotion_type = promotion_type

        if promotion_type == const.PROMOTION_TYPE_PRODUCT:
            data = form_data['promotion_type_product']
            promotion.product_type = data['product_type']
            promotion.promotion_implement_type = data['promotion_implement_type']
            promotion.above_the_price = data['above_the_price']
            promotion.percent = data['percent']
            promotion.price = data['price']
            promotion.above_the_number = data['above_the_number']
            if data['promotion_implement_type'] == \
                    const.PROMOTION_IMPLEMENT_TYPE_ABOVE_THE_NUMBER:
                promotion.percent = data['above_the_number_percent']
            promotion.save()
            promotion.products.clear()
            for product in form_data['promotion_type_product']['products']:
                promotion.products.add(product)

        elif promotion_type == const.PROMOTION_TYPE_PACKAGE:
            data = form_data['promotion_type_package']
            promotion.promotion_implement_type = const.PROMOTION_IMPLEMENT_TYPE_PERCENT
            promotion.quantity = data['quantity']
            promotion.percent = data['percent']
            promotion.save()
            promotion_type_package_formset = form_dict['promotion_type_package_formset']
            promotion_type_package_formset.save()

        elif promotion_type == const.PROMOTION_TYPE_SUPPLIER:
            data = form_data['promotion_type_supplier']
            promotion.supplier = data['supplier']
            promotion.product_type = data['product_type']
            promotion.above_the_price = data['above_the_price']
            promotion.promotion_implement_type = data['promotion_implement_type']
            promotion.percent = data['percent']
            promotion.price = data['price']
            promotion.above_the_number = data['above_the_number']
            if data['promotion_implement_type'] == 3:
                promotion.percent = data['above_the_number_percent']
            promotion.save()
            promotion.products.clear()
            for product in data['products']:
                promotion.products.add(product)

        elif promotion_type == const.PROMOTION_TYPE_ACC:
            promotion.save()
            promotion_type_acc = form_dict['promotion_type_acc']
            promotion_type_acc.save()

        if implement_type == const.IMPLEMENT_TYPE_CUSTOMER_CATEGORY:
            idata = form_data['implement_type_customer_category']
            for customer_category in idata['customer_categories']:
                promotion.customer_categories.add(customer_category)
                promotion.is_implement = idata['is_implement']
                promotion.save()

        elif implement_type == const.IMPLEMENT_TYPE_CUSTOMER:
            idata = form_data['implement_type_customer']
            for customer in idata['customers']:
                promotion.customers.add(customer)
                promotion.is_implement = idata['is_implement']
                promotion.save()

        elif implement_type == const.IMPLEMENT_TYPE_WAREHOUSE:
            idata = form_data['implement_type_warehouse']
            for warehouse in idata['warehouses']:
                promotion.warehouses.add(warehouse)
                promotion.is_implement = idata['is_implement']
                promotion.save()

        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа.')
        actions.log_update(self.request, promotion)
        return redirect('employee-promotion-list')


class PromotionDetail(c.DetailView):
    model = Promotion
    template_name = 'employee/promotion/detail.html'


class PromotionHistory(c.DetailView):
    model = Promotion
    template_name = 'employee/core/history.html'

    def get_context_data(self, **kwargs):
        context = super(PromotionHistory, self).get_context_data(**kwargs)
        obj = self.object
        context['action_list'] = LogEntry.objects.filter(
            content_type_id=ContentType.objects.get_for_model(obj).pk, object_id=obj.pk)
        return context


class PromotionDelete(c.RedirectView):
    """
    DeleteView
    """
    url = reverse_lazy('employee-promotion-list')

    def get_redirect_url(self, *args, **kwargs):
        promotion = get_object_or_404(Promotion, pk=self.kwargs['pk'])
        promotion.is_active = False
        promotion.save()
        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа')
        actions.log_delete(self.request, promotion)
        return super().get_redirect_url(*args, **kwargs)


def load_products(request):
    print("test")
    if request.is_ajax:
        print("test")
        seller_id = request.GET.get('seller_id')
        products = Product.objects.filter(seller__id=seller_id)
        print(products)
    return render(request, 'employee/promotion/ajax/products.html', {'products': products})
