# Generated by Django 2.2.4 on 2019-10-14 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Нэр')),
                ('flag', models.IntegerField()),
                ('is_active', models.BooleanField(default=True, verbose_name='Идэвхитэй')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Үүссэн огноо')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Зассан огноо')),
            ],
            options={
                'verbose_name': 'Албан тушаал',
                'verbose_name_plural': 'Албан тушаалууд',
                'ordering': ['-updated_at', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_name', models.CharField(max_length=128, null=True, verbose_name='Ургын овог')),
                ('last_name', models.CharField(max_length=128, null=True, verbose_name='Овог')),
                ('first_name', models.CharField(max_length=128, null=True, verbose_name='Өөрийн нэр')),
                ('register_no', models.CharField(max_length=128, null=True, verbose_name='Регистерийн дугаар')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Имэйл')),
                ('birth_date', models.CharField(max_length=62, null=True, verbose_name='Төрсөн огноо')),
                ('gender', models.IntegerField(choices=[(1, 'Эр'), (2, 'Эм')], null=True, verbose_name='Хүйс')),
                ('is_super_manager', models.BooleanField(help_text='Бүх компаний мэдээлэл харах боломжтой', verbose_name='Удирдлагын төлөв')),
                ('flag', models.IntegerField()),
                ('is_active', models.BooleanField(default=True, verbose_name='Идэвхитэй')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Үүссэн огноо')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Зассан огноо')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='managers', to='company.Company', verbose_name='Хариуцах компани')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='managers', to='employee.Position', verbose_name='Албан тушаал')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Хэрэглэгч')),
                ('warehouses', models.ManyToManyField(blank=True, to='warehouse.Warehouse', verbose_name='Хариуцах агуулахууд')),
            ],
            options={
                'verbose_name': 'Ажилтан',
                'verbose_name_plural': 'Ажилтнууд',
                'ordering': ['-updated_at', 'id'],
            },
        ),
    ]
