# -*- coding:utf-8 -*-

"""
Employee Form
"""

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from src.warehouse.models import Warehouse
from src.employee.models import Employee


__all__ = ['EmployeeCreateForm', 'EmployeeUpdateForm', 'EmployeeFilterForm']


class EmployeeCreateForm(forms.ModelForm):
    """
    EmployeeCreateForm
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'username_exists': _("Нэвтрэх нэр үүссэн байна."),
    }
    username = UsernameField(label='Нэвтрэх нэр')
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Employee
        fields = ['username', 'last_name', 'first_name', 'email', 'password1',
                  'password2', 'is_super_manager', 'company', 'warehouses']

    def __init__(self, *args, **kwargs):
        super(EmployeeCreateForm, self).__init__(*args, **kwargs)
        self.fields['warehouses'].queryset = Warehouse.objects.none()

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['warehouses'].queryset = Warehouse.objects.filter(
                    company_id=company_id)
            except (ValueError, TypeError):
                pass

    def clean_username(self):
        """
        to check username is unique
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists'
            )
        return username

    def clean_password2(self):
        """
        to check password1 password2 same
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        employee = super().save(commit=False)
        user = User(username=self.cleaned_data['username'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            employee.user = user
            employee.flag = 1
            employee.save()
        return user


class EmployeeUpdateForm(forms.ModelForm):
    """
    EmployeeUpdateForm.
    """

    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'email',
                  'is_super_manager', 'company', 'warehouses']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['warehouses'].queryset = Warehouse.objects.none()

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['warehouses'].queryset = Warehouse.objects.filter(
                    company_id=company_id)
            except (ValueError, TypeError):
                pass

        elif self.instance.pk and self.instance.company:
            self.fields['warehouses'].queryset = self.instance.company.warehouses


class EmployeeFilterForm(forms.Form):
    """
    EmployeeFilterForm
    """
    choices = (
        ('', 'Бүгд'),
        ('0', 'Админ'),
        ('1', 'Дотоод хэрэглэгч'),
    )
    username = forms.CharField()
    name = forms.CharField()
    email = forms.CharField()
    is_admin = forms.ChoiceField(choices=choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].required = False
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-sm'})
