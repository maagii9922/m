# -*- coding:utf8 -*-

from django.urls import path
from . import views as v


app_name = 'product'
urlpatterns = [
    path('categories/', v.CategoriesAPI.as_view(), name='categories'),

    path('list/', v.ProductsAPI.as_view(), name='products'),
    path('<int:id>/detail/', v.ProductDetailAPI.as_view(), name='product-detail'),
    path('new/', v.NewProductsAPI.as_view(), name='new-products'),

]
