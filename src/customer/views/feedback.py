

from django.contrib import messages
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

from src.feedback.models import Feedback


@require_POST
def create_feedback(request):
    feedback = Feedback.objects.create(
        user=request.user,
        subject=request.POST.get('subject'),
        message=request.POST.get('message')
    )
    messages.success(
        request, 'Таны хүсэлтийг хүлээн авлаа, Бидний ажилд үнэлгээ өгсөн танд баярлалаа.')
    return redirect('customer-home')
