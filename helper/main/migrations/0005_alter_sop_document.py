# Generated by Django 4.0.5 on 2024-04-19 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_ecn_desc_alter_sop_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sop',
            name='document',
            field=models.FileField(blank=True, upload_to='Documents/KB/SOP'),
        ),
    ]
