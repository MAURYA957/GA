# Generated by Django 4.0.5 on 2022-07-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(max_length=200, null=True)),
                ('Email', models.CharField(max_length=200, null=True)),
                ('Phone', models.CharField(max_length=200, null=True)),
                ('usertype', models.IntegerField(choices=[(0, 'Select'), (1, 'Ops Engineer'), (2, 'Supervisor'), (3, 'RC_Technician'), (4, 'Pilot')], default=0)),
                ('Password', models.CharField(max_length=128, verbose_name='password')),
                ('profilePic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('Createdate', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
