# Generated by Django 2.2.4 on 2019-10-24 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0008_auto_20191023_1335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotion',
            options={'ordering': ['order', '-id'], 'verbose_name': 'Урамшуулал', 'verbose_name_plural': 'Урамшуулаллууд'},
        ),
    ]
