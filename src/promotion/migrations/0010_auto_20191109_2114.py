# Generated by Django 2.2.4 on 2019-11-09 21:14

import django.core.validators
from django.db import migrations, models
import src.core.validate


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0009_auto_20191024_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='above_the_number',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Тооноос дээш'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='above_the_price',
            field=models.PositiveIntegerField(blank=True, help_text='Тухайн үнээс дээш худалдан авалт хийсэн үед урамшуулал хэрэгжинэ', null=True, verbose_name='Үнийн дүнгээс дээш'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='percent',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(99.9)], verbose_name='Хувь'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.1)], verbose_name='Үнэ'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='quantity',
            field=models.PositiveIntegerField(help_text='Дээрхид утга оруулснаар багцад хамаарах бүтээгдэхүүнүүдийн нийт тоо хэмжээ хүрэх үед урамшуулал хэрэгжинэ', null=True, validators=[src.core.validate.validate_nonzero], verbose_name='Багцийн тоо хэмжээ'),
        ),
        migrations.AlterField(
            model_name='promotionproduct',
            name='quantity',
            field=models.PositiveIntegerField(default=1, null=True, validators=[src.core.validate.validate_nonzero], verbose_name='Тоо хэмжээ'),
        ),
    ]
