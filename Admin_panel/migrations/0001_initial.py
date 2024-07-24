# Generated by Django 5.0.4 on 2024-07-18 07:56

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(default='waheed', max_length=200)),
                ('email', models.EmailField(default='', max_length=55)),
                ('phone', models.CharField(max_length=15)),
                ('joining_date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(default='waheed', max_length=200)),
                ('order_date', models.DateField(default=datetime.date.today)),
                ('amount', models.PositiveBigIntegerField(default=1)),
                ('payment_method', models.CharField(choices=[('Mastercard', 'Mastercard'), ('Visa', 'Visa'), ('PayPal', 'PayPal'), ('Cash on Delivery', 'Cash on Delivery'), ('Other', 'Other')], default='Mastercard', max_length=55)),
                ('delivery_status', models.CharField(choices=[('active', 'Active'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='active', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=150, unique=True)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=1.0, max_digits=10)),
                ('orders', models.PositiveIntegerField(default=1)),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=55)),
                ('last_name', models.CharField(default='', max_length=55)),
                ('email', models.EmailField(default='', max_length=55)),
                ('phone', models.CharField(default='', max_length=15)),
                ('address', models.CharField(default='', max_length=255)),
                ('country', models.CharField(default='', max_length=55)),
                ('state', models.CharField(default='', max_length=55)),
                ('zipcode', models.CharField(default='', max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total_amount', models.PositiveIntegerField()),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.order')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.customer')),
                ('order_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.orderdetail')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.product'),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], default='S', max_length=2)),
                ('color', models.CharField(choices=[('BL', 'Blue'), ('GR', 'Green'), ('RD', 'Red'), ('YL', 'Yellow'), ('BK', 'Black'), ('WH', 'White'), ('OR', 'Orange')], default='BK', max_length=2)),
                ('revenue', models.PositiveBigIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.product')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin_panel.productdetail'),
        ),
    ]
