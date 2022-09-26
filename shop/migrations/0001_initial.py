# Generated by Django 4.1.1 on 2022-09-22 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Category name')),
                ('img_url', models.ImageField(max_length=50, upload_to='category_images/')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Product name')),
                ('description', models.CharField(max_length=250, verbose_name='Description')),
                ('price', models.IntegerField(default=0, verbose_name='Price')),
                ('in_stock', models.IntegerField(default=0, verbose_name='In stock')),
                ('img', models.ImageField(upload_to='uploads/')),
                ('content_type', models.ForeignKey(default=50, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Blender',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.product')),
                ('volume', models.IntegerField(default=1, verbose_name='Volume')),
                ('fan_speed', models.IntegerField(default=500, verbose_name='Fan speed')),
            ],
            options={
                'verbose_name': 'Blender',
                'verbose_name_plural': 'Blenders',
            },
            bases=('shop.product',),
        ),
        migrations.CreateModel(
            name='Combine',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.product')),
                ('volume', models.IntegerField(default=2, verbose_name='Volume')),
                ('max_power', models.IntegerField(default=50, verbose_name='Power')),
            ],
            options={
                'verbose_name': 'Combine',
                'verbose_name_plural': 'Combines',
            },
            bases=('shop.product',),
        ),
        migrations.CreateModel(
            name='Fridge',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.product')),
                ('height', models.IntegerField(default=100, verbose_name='Height')),
                ('width', models.IntegerField(default=50, verbose_name='Width')),
                ('length', models.IntegerField(default=60, verbose_name='Length')),
            ],
            options={
                'verbose_name': 'Fridge',
                'verbose_name_plural': 'Fridges',
            },
            bases=('shop.product',),
        ),
        migrations.CreateModel(
            name='Mixer',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.product')),
                ('mixer_type', models.CharField(max_length=50, verbose_name='Mixer type')),
                ('fan_speed', models.IntegerField(default=1000, verbose_name='Fan speed')),
                ('bowl_size', models.IntegerField(default=5, verbose_name='Bowl size')),
            ],
            options={
                'verbose_name': 'Mixer',
                'verbose_name_plural': 'Mixers',
            },
            bases=('shop.product',),
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.product')),
                ('height', models.IntegerField(default=100, verbose_name='Height')),
                ('width', models.IntegerField(default=50, verbose_name='Width')),
                ('length', models.IntegerField(default=60, verbose_name='Length')),
            ],
            options={
                'verbose_name': 'Panel',
                'verbose_name_plural': 'Panels',
            },
            bases=('shop.product',),
        ),
        migrations.CreateModel(
            name='Teapot',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.product')),
                ('volume', models.IntegerField(default=2, verbose_name='Volume')),
                ('max_power', models.IntegerField(default=70, verbose_name='Power')),
            ],
            options={
                'verbose_name': 'Teapot',
                'verbose_name_plural': 'Teapots',
            },
            bases=('shop.product',),
        ),
    ]
