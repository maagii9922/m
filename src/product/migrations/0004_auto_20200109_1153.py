# Generated by Django 2.2.4 on 2020-01-09 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20191119_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='in_stock',
            field=models.FloatField(verbose_name='Барааны тоо хэмжээ'),
        ),
    ]
