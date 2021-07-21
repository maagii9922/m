# -*- coding:utf8 -*-
"""
Бүтээгдэхүүнтэй холбоотой сервис
"""

from rest_framework import generics

from src.product.models import Category, Product

from .serializers import CategorySerializer, ProductSerializer


class CategoriesAPI(generics.ListAPIView):
    """
    Толгой ангиллын жагсаалт гаргах сервис
    """
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer


class NewProductsAPI(generics.ListAPIView):
    '''
    Нүүр хуудсанд харагдах шинэ 5 мэдээлэл гаргах сервис
    '''
    queryset = Product.objects.filter(
        flag=1).exclude(image='')[:4]
    serializer_class = ProductSerializer


class ProductsAPI(generics.ListAPIView):
    """
    Бүтээгдэхүүний жагсаалт
    """
    queryset = Product.objects.exclude(image='')[:30]
    serializer_class = ProductSerializer


class ProductDetailAPI(generics.RetrieveAPIView):
    '''
    Бүтээгдэхүүний дэлгэрэнгүй
    '''
    lookup_field = 'id'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
