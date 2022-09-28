# Generated by Django 4.1.1 on 2022-09-28 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, to='shop.product', verbose_name='Product name'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='cart.orderitem'),
        ),
    ]
