# -*- coding:utf-8 -*-

"""POST"""
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages

from src.post.models import Post
from src.employee.forms import PostFilterForm
from . import core as c


__all__ = ['PostList', 'PostCreate', 'PostUpdate', 'PostDelete']


class PostList(c.ListView):
    """
    PostList
    """
    queryset = Post.objects.filter(is_active=True)
    page_title = 'Нийтлэл'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Нийтлэл', ''),
    ]
    add_url = reverse_lazy('employee-post-create')
    filter_form = PostFilterForm
    fields = ['get_category_name', 'title', 'author',
              'updated_at', 'get_is_published_html']
    paginate_by = 20

    def get_queryset(self):
        category = self.request.GET.get("category")
        title = self.request.GET.get("title")
        author = self.request.GET.get("author")
        dates = self.request.GET.get("dates")
        status = self.request.GET.get("status")
        queryset = super().get_queryset()
        if category:
            queryset = queryset.filter(category=category)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author=author)
        if dates:
            dates = dates.split(" - ")
            queryset = queryset.filter(updated_at__date__range=dates)
        if status == '0':
            queryset = queryset.filter(is_published=False)
        elif status == '1':
            queryset = queryset.filter(is_published=True)
        return queryset


class PostCreate(c.CreateView):
    model = Post
    fields = ['category', 'title', 'background_image', 'content']
    template_name = 'employee/post/edit.html'
    success_url = reverse_lazy('employee-post-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Нийтлэл нэмэх'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Нийтлэл', reverse_lazy('employee-post-list')),
            ('Нийтлэл нэмэх', ''),
        ]
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        if self.request.POST.get('save'):
            obj.is_published = False
        return super().form_valid(form)


class PostUpdate(c.UpdateView):
    """
    PostUpdate
    """
    model = Post
    fields = ['category', 'title', 'background_image', 'content']
    template_name = 'employee/post/edit.html'
    success_url = reverse_lazy('employee-post-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Нийтлэл засах'
        context['breadcrumbs'] = [
            ('Хянах самбар', reverse_lazy('employee-dashboard')),
            ('Нийтлэл', reverse_lazy('employee-post-list')),
            ('Нийтлэл засах', ''),
        ]
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.POST.get('publish'):
            obj.is_published = True
        return super().form_valid(form)


class PostDelete(c.RedirectView):
    """
    PostDelete
    """
    url = reverse_lazy('employee-post-list')

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        post.is_active = False
        post.save()
        messages.success(self.request, 'Мэдээлэл амжилттай хадгалагдлаа')
        return super().get_redirect_url(*args, **kwargs)
