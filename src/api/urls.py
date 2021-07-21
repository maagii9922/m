# -*- coding:utf8 -*-

from django.urls import path, include


urlpatterns = [
    path('authenticate/', include('src.api.authenticate.urls')),
    path('post/', include('src.api.post.urls')),
    path('feedback/', include('src.api.feedback.urls')),
    path('product/', include('src.api.product.urls')),
]
