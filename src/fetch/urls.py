# -*- coding:utf-8 -*-

"""
ИРП-с мэдээлэл татах url
"""

from django.urls import path
from . import views as v

app_name = 'fetch'


urlpatterns = [

    path('', v.home, name='home'),

    path('update-company/', v.update_company, name='update_company'),

    path('update-branch/', v.update_warehouse, name='update_warehouse'),

    path('update-customer/', v.update_customer,
         name='update_customer'),

    path('update-position/', v.update_position, name='update_position'),
    path('update-employee/', v.update_employee, name='update_employee'),

    path('update-company-customer/', v.update_company_customer,
         name='update_company_customer'),

    path('update-product-category/', v.update_product_category,
         name='update_product_category'),

    path('update-measuring-type/', v.update_measuring_type,
         name='update_measuring_type'),

    path('update-product-form/', v.update_product_form,
         name='update_product_form'),

    path('update-product/', v.update_product, name='update_product'),

    path('update-product-price/', v.update_product_price,
         name='update_product_price'),

    path('update-company-warehouse-product-price/<int:company_id>/<int:warehouse_id>/', v.update_company_warehouse_product_price,
         name='update_company_warehouse_product_price'),

    path('update-company-warehouse-product-stock/<int:warehouse_id>/', v.update_company_warehouse_product_stock,
         name='update_company_warehouse_product_stock'),

    path('update-product-stock/', v.update_product_stock,
         name='update_product_stock'),
    path('order/', v.order, name='order')
]
