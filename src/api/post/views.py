from rest_framework import generics, permissions

from src.post.models import Post

from .serializers import PostSerializer


class HomePostsAPI(generics.ListAPIView):
    '''
    Нүүр хуудсанд харагдах 3 мэдээлэл гаргах сервис
    '''
    queryset = Post.objects.filter(is_published=True, is_active=True)[:3]
    serializer_class = PostSerializer


class PostsAPI(generics.ListAPIView):
    '''
    Мэдээллийн жагсаалт гаргах сервис
    '''
    queryset = Post.objects.filter(is_published=True, is_active=True)
    serializer_class = PostSerializer


class PostDetailAPI(generics.RetrieveAPIView):
    '''
    Мэдээллийн дэлгэрэнгүй гаргах сервис
    '''
    lookup_field = 'id'
    queryset = Post.objects.filter(is_published=True, is_active=True)
    serializer_class = PostSerializer
