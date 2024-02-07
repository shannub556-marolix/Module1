# Generated by Django 5.0.1 on 2024-01-12 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0004_product_prod_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bestseller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pcode', models.IntegerField()),
                ('pname', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('mfd', models.CharField(max_length=100)),
                ('exp', models.CharField(max_length=20)),
                ('prod_count', models.IntegerField(default=0)),
            ],
        ),
    ]