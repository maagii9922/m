# Generated by Django 2.2.4 on 2019-10-14 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('customer', '0001_initial'),
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Нэр')),
                ('start_date', models.DateTimeField(verbose_name='Урамшуулал эхлэх огноо')),
                ('end_date', models.DateTimeField(verbose_name='Урамшуулал дуусах огноо')),
                ('calculation_type', models.BooleanField(default=True, verbose_name='Тооцоолох төрөл')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Хэрэгжүүлэх дараалал')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Тайлбар')),
                ('promotion_type', models.IntegerField(choices=[(1, 'Бүтээгдэхүүн'), (2, 'Багц'), (3, 'Нийлүүлэгч'), (4, 'Акц')], verbose_name='Урамшууллын төрөл')),
                ('promotion_implement_type', models.IntegerField(choices=[(1, 'Хувь'), (2, 'Үнэ'), (3, 'Тооноос дээш')], verbose_name='Урамшуулал хэрэгжих төрөл')),
                ('above_the_price', models.IntegerField(blank=True, null=True, verbose_name='Үнийн дүнгээс дээш')),
                ('percent', models.FloatField(blank=True, null=True, verbose_name='Хувь')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Үнэ')),
                ('above_the_number', models.IntegerField(blank=True, null=True, verbose_name='Тооноос дээш')),
                ('quantity', models.IntegerField(null=True, verbose_name='Багцийн тоо хэмжээ')),
                ('implement_type', models.IntegerField(choices=[(1, 'Бүгд'), (2, 'Харилцагчийн төрөл'), (3, 'Харилцагчид'), (4, 'Агуулах')], verbose_name='Харилцагчид хэрэгжүүлэх төрөл')),
                ('is_implement', models.BooleanField(default=True, verbose_name='Хэрэгжүүлнэ/Хэрэгжүүлэхгүй')),
                ('is_active', models.BooleanField(default=True, verbose_name='Идэвхитэй')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Үүссэн огноо')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Зассан огноо')),
                ('customer_categories', models.ManyToManyField(blank=True, related_name='promotions', to='customer.CustomerCategory', verbose_name='Харилцагчийн төрөл')),
                ('customers', models.ManyToManyField(blank=True, related_name='promotions', to='customer.Customer', verbose_name='Харилцагчид')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supplier_promotions', to='customer.Customer', verbose_name='Нийлүүлэгч')),
                ('warehouses', models.ManyToManyField(blank=True, related_name='promotions', to='warehouse.Warehouse', verbose_name='Агуулах')),
            ],
            options={
                'verbose_name': 'Урамшуулал',
                'verbose_name_plural': 'Урамшуулаллууд',
                'ordering': ['order', '-updated_at', 'id'],
            },
        ),
        migrations.CreateModel(
            name='PromotionProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True, verbose_name='Тоо хэмжээ')),
                ('is_not_bonus', models.BooleanField(default=True, verbose_name='Авах/Өгөх')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotion_products', to='product.Product', verbose_name='Бүтээгдэхүүн')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotion_products', to='promotion.Promotion', verbose_name='Урамшуулал')),
            ],
            options={
                'verbose_name': 'Урамшууллын бүтээгдэхүүн',
                'verbose_name_plural': 'Урамшууллын бүтээгдэхүүнүүд',
            },
        ),
    ]
