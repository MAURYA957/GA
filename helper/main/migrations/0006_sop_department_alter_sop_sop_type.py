# Generated by Django 4.0.5 on 2024-04-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_sop_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='sop',
            name='department',
            field=models.CharField(choices=[('1', 'None'), ('2', 'Planner'), ('3', 'Embedded'), ('4', 'Ga_app'), ('5', 'FCS'), ('6', 'Hardware'), ('7', 'Other')], default=1, max_length=50),
        ),
        migrations.AlterField(
            model_name='sop',
            name='sop_type',
            field=models.CharField(choices=[('1', 'None'), ('2', 'Software'), ('3', 'Hardware'), ('4', 'QC'), ('5', 'Others')], default=1, max_length=20),
        ),
    ]