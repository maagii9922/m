# Generated by Django 2.2.4 on 2020-01-09 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20191119_1709'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderproduct',
            options={'ordering': ['product__name'], 'verbose_name': 'Захиалгын бүтээгдэхүүн', 'verbose_name_plural': 'Захиалгын бүтээгдэхүүнүүд'},
        ),
    ]
