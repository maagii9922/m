from rest_framework import serializers

from src.feedback.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'subject', 'message')
