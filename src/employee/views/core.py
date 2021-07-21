# -*- coding=utf-8 -*-

from datetime import date

from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as AuthLoginView, LogoutView as AuthLogoutView)
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic as g
from django.urls import reverse_lazy

from formtools.wizard.views import SessionWizardView as FormtoolsSessionWizardView


from src.order.models import Order
from src.customer.models import Customer

from src.employee.forms import LoginForm


__all__ = ['Dashboard', 'Login', 'Logout']


class LoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('employee-login')

    def dispatch(self, request, *args, **kwargs):
        # Хэрэглэгч нэвтрээгүй эсвэл хэрэглэгч employee атрибут байхгүй эсвэл
        # хэрэглэгчийн ажилтан идэвхигүй байвал хэрэглэгчийг системээс гаргана
        if not request.user.is_authenticated or not hasattr(request.user, 'employee') \
                or not request.user.employee.is_active:
            if request.user:
                logout(request)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class TemplateView(LoginRequired, g.TemplateView):
    pass


class ListView(LoginRequired, g.ListView):
    template_name = 'employee/core/list.html'
    page_title = None
    breadcrumbs = None
    add_url = None
    filter_form = None
    fields = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page_title:
            context['page_title'] = self.page_title
        else:
            raise ImproperlyConfigured('page_title заавал утгатай байна')
        if self.breadcrumbs:
            context['breadcrumbs'] = self.breadcrumbs
        else:
            raise ImproperlyConfigured('breadcrumbs заавал утгатай байна')
        if self.add_url:
            context['add_url'] = self.add_url
        if self.filter_form:
            context['filter_form'] = self.filter_form(self.request.GET)
        else:
            raise ImproperlyConfigured('filter_form заавал утгатай байна')
        if self.fields:
            context['fields'] = self.fields
        else:
            raise ImproperlyConfigured('fields заавал утгатай байна')
        return context


class FormView(LoginRequired, SuccessMessageMixin, g.FormView):
    success_message = 'Мэдээлэл амжилттай хадгалагдлаа'


class CreateView(LoginRequired, SuccessMessageMixin, g.CreateView):
    success_message = 'Мэдээлэл амжилттай хадгалагдлаа'


class UpdateView(LoginRequired, SuccessMessageMixin, g.UpdateView):
    success_message = 'Мэдээлэл амжилттай хадгалагдлаа'


class DeleteView(LoginRequired, SuccessMessageMixin, g.DeleteView):
    success_message = 'Мэдээлэл амжилттай хадгалагдлаа'


class RedirectView(LoginRequiredMixin, SuccessMessageMixin, g.RedirectView):
    success_message = 'Мэдээлэл амжилттай хадгалагдлаа'


class DetailView(LoginRequired, g.DetailView):
    pass


class SessionWizardView(LoginRequired, FormtoolsSessionWizardView):
    page_title = None
    breadcrumbs = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page_title:
            context['page_title'] = self.page_title
        else:
            raise ImproperlyConfigured('page_title заавал утгатай байна')
        if self.breadcrumbs:
            context['breadcrumbs'] = self.breadcrumbs
        else:
            raise ImproperlyConfigured('breadcrumbs заавал утгатай байна')
        return context


class Dashboard(TemplateView):
    template_name = 'employee/core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['today_order_count'] = Order.objects.filter(
            created_at__date=date.today(), is_active=True).count()
        context['all_order_count'] = Order.objects.filter(
            is_active=True).count()
        context['registered_customer_count'] = Customer.objects.filter(
            user__isnull=False).count()
        context['all_customer_count'] = Customer.objects.filter(
            company__isnull=False).count()
        return context


class Login(AuthLoginView):
    form_class = LoginForm
    template_name = 'employee/core/login.html'


class Logout(AuthLogoutView):
    next_page = reverse_lazy('employee-login')
