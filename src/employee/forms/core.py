# -*- coding=utf-8 -*-

"""
Core
"""

from django.contrib.auth.forms import AuthenticationForm


__all__ = ['LoginForm']


class LoginForm(AuthenticationForm):
    """
    LoginForm
    """

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Нэвтрэх нэр'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Нууц үг'})

    def clean(self):
        cleaned_data = super().clean()
        if not self.user_cache.employee.is_active:
            self.add_error('', 'Хэрэглэгч хандах эрхгүй байна')
        return cleaned_data
