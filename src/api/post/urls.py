from django.urls import path
from . import views as v


app_name = 'post'
urlpatterns = [
    path('', v.PostsAPI.as_view(), name='posts'),
    path('<int:id>/detail/', v.PostDetailAPI.as_view(), name='post-detail'),
    path('home/', v.HomePostsAPI.as_view(), name='home-posts'),
]
