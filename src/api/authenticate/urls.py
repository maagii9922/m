# -*- coding:utf8 -*-

from django.urls import path

from . import views as v


app_name = 'authenticate'
urlpatterns = [
    path('login/', v.LoginAPI.as_view(), name='login'),
    path('user/', v.UserAPI.as_view(), name='user'),
]
