# Generated by Django 2.2.4 on 2019-10-21 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0006_auto_20191017_0944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotion',
            options={'ordering': ['order', 'id'], 'verbose_name': 'Урамшуулал', 'verbose_name_plural': 'Урамшуулаллууд'},
        ),
    ]
