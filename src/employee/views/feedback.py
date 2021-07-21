

from django.urls import reverse_lazy

from src.feedback.models import Feedback
from src.employee.views.core import ListView
from src.employee.forms import FeedbackFilterForm


__all__ = ['Feedbacks']


class Feedbacks(ListView):
    model = Feedback
    page_title = 'Санал хүсэлт'
    breadcrumbs = [
        ('Хянах самбар', reverse_lazy('employee-dashboard')),
        ('Санал хүсэлт', ''),
    ]
    filter_form = FeedbackFilterForm
    fields = ['user', 'subject', 'message', 'created_at']
