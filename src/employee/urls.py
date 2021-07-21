# -*- coding=utf-8 -*-


"""
Employee url
"""


from django.urls import path

from src.core.urls import Nurl

from . import views as v


urlpatterns = [
    Nurl('') > 'src.employee.views.Dashboard',
    Nurl('login/') > 'src.employee.views.Login',
    Nurl('logout/') > 'src.employee.views.Logout',

    Nurl('employee/') > 'src.employee.views.List',
    Nurl('employee/create/') > 'src.employee.views.Create',
    Nurl('employee/<int:pk>/update/') > 'src.employee.views.Update',
    Nurl('employee/<int:pk>/delete/') > 'src.employee.views.Delete',
    Nurl('employee/<int:employee_pk>/user/create/') > 'src.employee.views.UserCreate',
    Nurl('employee/<int:pk>/user/update/') > 'src.employee.views.UserUpdate',
    path('ajax/load-warehouses/', v.load_warehouses,
         name='employee-ajax-load-warehouses'),

    Nurl('customers/') > 'src.employee.views.CustomerList',
    Nurl('customers/<int:pk>/update/') > 'src.employee.views.CustomerUpdate',
    Nurl('customers/<int:pk>/active/') > 'src.employee.views.CustomerActive',
    Nurl('customers/<int:pk>/delete/') > 'src.employee.views.CustomerDelete',
    Nurl('customers/user/<int:pk>/create/') > 'src.employee.views.CustomerUserCreate',
    Nurl('customers/user/<int:pk>/update/') > 'src.employee.views.CustomerUserUpdate',

    Nurl('promotions/') > 'src.employee.views.PromotionList',
    Nurl('promotions/create/') > 'src.employee.views.PromotionCreate',
    Nurl('promotions/<int:pk>/update/') > 'src.employee.views.PromotionUpdate',
    Nurl('promotions/<int:pk>/detail/') > 'src.employee.views.PromotionDetail',
    Nurl('promotions/<int:pk>/history/') > 'src.employee.views.PromotionHistory',
    Nurl('promotions/<int:pk>/delete/') > 'src.employee.views.PromotionDelete',
    path('ajax/load-products/', v.load_products,
         name='promotion-ajax-load-products'),

    Nurl('advertisements/') > 'src.employee.views.AdvertisementList',
    Nurl('advertisements/create/') > 'src.employee.views.AdvertisementCreate',
    Nurl('advertisements/<int:pk>/update/') > 'src.employee.views.AdvertisementUpdate',
    Nurl('advertisements/<int:pk>/detail/') > 'src.employee.views.AdvertisementDetail',
    Nurl('advertisements/<int:pk>/history/') > 'src.employee.views.AdvertisementHistory',
    Nurl('advertisements/<int:pk>/delete/') > 'src.employee.views.AdvertisementDelete',

    Nurl('posts/') > 'src.employee.views.PostList',
    Nurl('posts/create/') > 'src.employee.views.PostCreate',
    Nurl('posts/<int:pk>/update/') > 'src.employee.views.PostUpdate',
    Nurl('posts/<int:pk>/delete/') > 'src.employee.views.PostDelete',

    Nurl('orders/') > 'src.employee.views.Orders',
    Nurl('orders/<int:pk>/detail/') > 'src.employee.views.OrderDetail',
    # Nurl('post/<str:slug>/delete/') > 'src.employee.views.PostDelete'
    Nurl('feedbacks') > 'src.employee.views.Feedbacks'
]
