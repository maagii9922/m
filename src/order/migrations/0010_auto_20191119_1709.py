# Generated by Django 2.2.4 on 2019-11-19 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20191109_2114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-updated_at'], 'verbose_name': 'Захиалга', 'verbose_name_plural': 'Захиалгууд'},
        ),
    ]
