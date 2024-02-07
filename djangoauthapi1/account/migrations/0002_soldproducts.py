# Generated by Django 5.0.1 on 2024-02-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoldProducts',
            fields=[
                ('product_code', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=200)),
                ('product_name', models.CharField(max_length=200)),
                ('product_expiry', models.CharField(max_length=200)),
                ('product_mfd', models.CharField(max_length=200)),
                ('product_waranty', models.CharField(max_length=200)),
                ('product_category', models.CharField(max_length=200)),
            ],
        ),
    ]
