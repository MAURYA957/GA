# Generated by Django 4.0.5 on 2024-04-19 13:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_sop_department_alter_sop_sop_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sop',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
