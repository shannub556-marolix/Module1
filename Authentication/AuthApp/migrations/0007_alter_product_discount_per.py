# Generated by Django 5.0.1 on 2024-01-23 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0006_alter_product_prod_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_per',
            field=models.CharField(default=0),
        ),
    ]