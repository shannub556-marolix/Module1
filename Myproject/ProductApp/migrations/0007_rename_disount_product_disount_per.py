# Generated by Django 5.0.1 on 2024-01-23 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0006_rename_price_product_original_price_product_disount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='disount',
            new_name='disount_per',
        ),
    ]