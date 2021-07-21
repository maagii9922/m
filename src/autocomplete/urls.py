# -*- coding:utf-8 -*-
"""
Autocomplete urls
"""

from src.core.urls import Nurl


urlpatterns = [
    Nurl('warehouses/') > 'src.autocomplete.views.Warehouses',
    Nurl('customer-categories/') > 'src.autocomplete.views.CustomerCategories',
    Nurl('customers/') > 'src.autocomplete.views.Customers',
    Nurl('suppliers/') > 'src.autocomplete.views.Suppliers',
    Nurl('products/') > 'src.autocomplete.views.Products'
]
