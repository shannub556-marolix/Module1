# Generated by Django 5.0.1 on 2024-01-23 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0005_rename_disount_per_product_discount_per'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_count',
            field=models.CharField(default=0),
        ),
    ]
