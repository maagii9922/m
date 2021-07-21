
from django import forms
from django.contrib.auth.models import User

from src.post.models import Post


__all__ = ['PostFilterForm']


class PostFilterForm(forms.ModelForm):
    STATUS_CHOICE = (
        ('', 'Бүгд'),
        ('0', 'Ноорог'),
        ('1', 'Нийтлэгдсэн')
    )

    status = forms.ChoiceField(choices=STATUS_CHOICE)
    date = forms.CharField()

    class Meta:
        model = Post
        fields = ['category', 'title', 'author', 'date', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = User.objects.filter(
            employee__isnull=False)
        for key in self.fields.keys():
            self.fields[key].required = False
            self.fields[key].widget.attrs.update(
                {'class': 'form-control form-control-sm'})
