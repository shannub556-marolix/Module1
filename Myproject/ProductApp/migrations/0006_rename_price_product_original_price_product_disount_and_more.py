# Generated by Django 5.0.1 on 2024-01-23 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0005_bestseller'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='original_price',
        ),
        migrations.AddField(
            model_name='product',
            name='disount',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='new_price',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
