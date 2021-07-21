
from django import forms

from src.feedback.models import Feedback


__all__ = ['FeedbackFilterForm']


class FeedbackFilterForm(forms.Form):
    user = forms.CharField()
    subject = forms.CharField()
    message = forms.CharField()
    created_at = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(FeedbackFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].widget.attrs.update(
                {'class': 'form-control form-control-sm'})
