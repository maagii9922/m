# Generated by Django 2.2.4 on 2019-10-15 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0003_auto_20191015_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='promotion_implement_type',
            field=models.IntegerField(choices=[(1, 'Хувь'), (2, 'Үнэ'), (3, 'Тооноос дээш')], null=True, verbose_name='Урамшуулал хэрэгжих төрөл'),
        ),
    ]
