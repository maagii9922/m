

from src.post.models import Post
from src.customer.views import core as c


__all__ = ['Posts', 'PostDetail']


class Posts(c.ListView):
    """
    Posts
    """
    model = Post
    template_name = 'customer/post/list.html'
    context_object_name = 'posts'
    paginate_by = 5


class PostDetail(c.DetailView):
    model = Post
    template_name = 'customer/post/detail.html'
    context_object_name = 'post'
