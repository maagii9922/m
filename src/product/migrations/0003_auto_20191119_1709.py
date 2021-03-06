# Generated by Django 2.2.4 on 2019-11-19 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20191025_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='eng_name',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Англи нэр'),
        ),
        migrations.AlterField(
            model_name='product',
            name='generic_name',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Олон улсын нэршил'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=512, verbose_name='Нэр'),
        ),
        migrations.AlterField(
            model_name='product',
            name='volume',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Эзлэхүүн'),
        ),
    ]
