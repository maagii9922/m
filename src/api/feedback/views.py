
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST)

from src.feedback.models import Feedback

from .serializers import FeedbackSerializer


class FeedbackAPI(APIView):
    permission_classes = []
    serializer_class = FeedbackSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            name = data['name']
            email = data['email']
            subject = data['subject']
            message = data['message']
            feedback = Feedback(name=name, email=email,
                                subject=subject, message=message)
            # feedback.save()
            print(feedback)
            print(feedback)
            print(feedback)
            print(feedback)
            print(feedback)
            return Response({'status': True}, status=HTTP_200_OK)
        return Response({'status': False}, status=HTTP_400_BAD_REQUEST)
