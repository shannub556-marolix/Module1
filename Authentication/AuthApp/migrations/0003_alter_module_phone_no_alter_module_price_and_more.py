# Generated by Django 5.0.1 on 2024-01-19 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthApp', '0002_module'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='phone_no',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='module',
            name='price',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='module',
            name='product_id',
            field=models.CharField(max_length=100),
        ),
    ]
