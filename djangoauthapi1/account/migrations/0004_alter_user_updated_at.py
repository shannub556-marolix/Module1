# Generated by Django 4.2.10 on 2024-02-15 05:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.CharField(default=datetime.datetime(2024, 2, 15, 10, 58, 8, 577172), max_length=200),
        ),
    ]
