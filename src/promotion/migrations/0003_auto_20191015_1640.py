# Generated by Django 2.2.4 on 2019-10-15 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0002_promotion_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='product_type',
            field=models.IntegerField(choices=[(1, 'Бүгд'), (2, 'Сонгосон бүтээгдэхүүнд хэрэгжинэ'), (3, 'Сонгосон бүтээгдэхүүнд хэрэгжихгүй')], null=True, verbose_name='Бүтээгдэхүүний төрөл'),
        ),
    ]
