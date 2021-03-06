# Generated by Django 2.2.4 on 2019-10-14 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Ангилал')),
            ],
            options={
                'verbose_name': 'Ангилал',
                'verbose_name_plural': 'Ангиллууд',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'Таг',
                'verbose_name_plural': 'Тагууд',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True, verbose_name='Гарчиг')),
                ('slug', models.SlugField(editable=False, max_length=256, unique=True, verbose_name='Слаг')),
                ('background_image', models.ImageField(upload_to='', verbose_name='Нүүр зураг')),
                ('content', tinymce.models.HTMLField(verbose_name='Агуулга')),
                ('is_published', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Идэвхитэй')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Үүссэн огноо')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Зассан огноо')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Нийтлэгч')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='post.Category', verbose_name='Ангилал')),
                ('tags', models.ManyToManyField(blank=True, related_name='posts', to='post.Tag', verbose_name='Тагууд')),
            ],
            options={
                'verbose_name': 'Нийтлэл',
                'verbose_name_plural': 'Нийтлэлүүд',
                'ordering': ['-updated_at', 'id'],
            },
        ),
    ]
