# Generated by Django 5.1 on 2024-08-27 14:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AddField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
