# Generated by Django 2.2.4 on 2019-10-14 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=256, verbose_name='Гарчиг')),
                ('message', models.TextField(verbose_name='Мессеж')),
                ('is_active', models.BooleanField(default=True, verbose_name='Идэвхитэй')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Үүссэн огноо')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Зассан огноо')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL, verbose_name='Хэрэглэгч')),
            ],
            options={
                'verbose_name': 'Санал хүсэлт',
                'verbose_name_plural': 'Санал хүсэлт',
                'ordering': ['-updated_at', 'id'],
            },
        ),
    ]
