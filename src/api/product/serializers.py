# -*- coding:utf-8 -*-

"""[summary]
"""

from rest_framework import serializers

from src.product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """[summary]

    Arguments:
        serializers {[type]} -- [description]
    """
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    """[summary]

    Arguments:
        serializers {[type]} -- [description]
    """
    class Meta:
        model = Product
        fields = ('id', 'image', 'category', 'name')
