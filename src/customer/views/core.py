# -*- coding:utf-8 -*-

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.views import generic as g
from django.urls import reverse_lazy
from django.shortcuts import render


__all__ = ['TemplateView', 'ListView', 'DetailView']


class LoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('customer-login')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'customer'):
            if request.user:
                logout(request)
            return self.handle_no_permission()
        return super(LoginRequired, self).dispatch(request, *args, **kwargs)


class TemplateView(LoginRequired, g.TemplateView):
    pass


class ListView(LoginRequired, g.ListView):
    pass


class DetailView(LoginRequired, g.DetailView):
    pass


# def handler404(request, exception):
#     return render(request, 'customer/404.html', status=404)
# def handler500(request):
#     return render(request, 'customer/500.html', status=500)

def error_404(request, exception):
    data = {}
    return render(request, 'certman/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'certman/500.html', data)
