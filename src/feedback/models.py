# -*- coding:utf-8 -*-

"""
Санал хүсэлт
"""


from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    """
    Санал хүсэлт
    """
    user = models.ForeignKey(
        User,
        verbose_name='Хэрэглэгч',
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    subject = models.CharField(verbose_name='Гарчиг', max_length=256)
    message = models.TextField(verbose_name='Мессеж')
    is_active = models.BooleanField(verbose_name='Идэвхитэй', default=True)
    created_at = models.DateTimeField(
        verbose_name='Үүссэн огноо', auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Зассан огноо', auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'id']
        verbose_name = 'Санал хүсэлт'
        verbose_name_plural = 'Санал хүсэлт'

    def __str__(self):
        return self.user.username
