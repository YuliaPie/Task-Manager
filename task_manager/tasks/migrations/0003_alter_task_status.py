# Generated by Django 5.0.7 on 2024-08-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(choices=[(3, 'Новый')], default=1),
        ),
    ]
