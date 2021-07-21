from django.urls import path

from .views import FeedbackAPI


app_name = 'feedback'
urlpatterns = [
    path('', FeedbackAPI.as_view(), name='feedback')
]
