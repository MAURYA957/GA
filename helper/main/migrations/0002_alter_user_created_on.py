# Generated by Django 4.0.5 on 2024-04-19 11:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
