# Generated by Django 2.2.4 on 2019-10-21 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20191021_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='discount_package',
            field=models.FloatField(null=True),
        ),
    ]
