# -*- coding:utf8 -*-

from rest_framework import serializers
from src.post.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title',
                  'background_image', 'content', 'updated_on')
