# Generated by Django 5.0.4 on 2024-07-20 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_panel', '0002_category_description_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='category_images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Admin_panel.category')),
            ],
        ),
    ]
