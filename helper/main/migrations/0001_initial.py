# Generated by Django 4.0.5 on 2024-04-17 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Partname', models.CharField(max_length=200, unique=True)),
                ('Partcode', models.CharField(max_length=100, unique=True)),
                ('Version', models.CharField(max_length=100, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='users/%Y/%M')),
            ],
        ),
        migrations.CreateModel(
            name='AllocatedCustomer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('AllocatedCustomer_name', models.CharField(max_length=20)),
                ('AllocatedCustomer_city', models.CharField(max_length=20)),
                ('AllocatedCustomer_address', models.CharField(max_length=100)),
                ('AllocatedCustomer_pincode', models.IntegerField()),
                ('AllocatedCustomer_contact', models.CharField(max_length=20)),
                ('AllocatedCustomer_email', models.EmailField(max_length=100)),
                ('AllocatedCustomer_Escalation_contact', models.CharField(max_length=20)),
                ('AllocatedCustomer_Escalation_email', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='users/%Y/%M')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=20)),
                ('pincode', models.IntegerField()),
                ('contact', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('Escalation_contact', models.CharField(max_length=20)),
                ('Escalation_email', models.EmailField(max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.country')),
            ],
        ),
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Drone_id', models.CharField(max_length=20, unique=True)),
                ('UIN', models.CharField(max_length=20, unique=True)),
                ('drone_type', models.CharField(choices=[('1', 'None'), ('2', 'Service'), ('3', 'Sold'), ('4', 'Training'), ('5', 'Others')], default=1, max_length=20)),
                ('AVB', models.CharField(max_length=20)),
                ('Timble_module', models.CharField(max_length=20)),
                ('Subscription_date', models.DateField()),
                ('Subscription_end_date', models.DateField()),
                ('Drone_base_version', models.CharField(max_length=20)),
                ('CC_base_version', models.CharField(max_length=20)),
                ('FCS_base_version', models.CharField(max_length=20)),
                ('BLL_base_version', models.CharField(max_length=20)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='image/product/')),
                ('spec', models.FileField(upload_to='documents/product/')),
                ('description', models.TextField()),
                ('created_on', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='image/productmodel/')),
                ('spec', models.FileField(upload_to='documents/productmodel/')),
                ('description', models.TextField()),
                ('created_on', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Warranty_type', models.CharField(choices=[('1', 'None'), ('2', 'Warranty'), ('3', 'AMC'), ('4', 'CMC'), ('5', 'Others')], default=1, max_length=20)),
                ('uin', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('dispatch_date', models.DateField()),
                ('delivery_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('dispatch_list', models.FileField(upload_to='documents/dispatch/')),
                ('handover_doc', models.FileField(upload_to='documents/handover/')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.drone')),
                ('primary_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('product_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.productmodel')),
                ('secondry_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.allocatedcustomer')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state_name', models.CharField(max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.country')),
            ],
        ),
        migrations.CreateModel(
            name='ECN',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('release', models.CharField(max_length=100)),
                ('Drone_version', models.CharField(max_length=100)),
                ('CC_version', models.CharField(max_length=100)),
                ('FCS_version', models.CharField(max_length=100)),
                ('BLL_version', models.CharField(max_length=100)),
                ('expertise', models.CharField(choices=[('1', 'None'), ('2', 'Pilot'), ('3', 'Technician'), ('4', 'Ops_Engineer'), ('5', 'Support_agent'), ('6', 'Developers')], default=1, max_length=10)),
                ('type', models.CharField(choices=[('1', 'None'), ('2', 'Software'), ('3', 'Hardware'), ('4', 'QC'), ('5', 'Others')], default=1, max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('department', models.CharField(choices=[('1', 'None'), ('2', 'Planner'), ('3', 'Embedded'), ('4', 'Ga_app'), ('5', 'FCS'), ('6', 'Hardware'), ('7', 'Other')], default=1, max_length=50)),
                ('release_by', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('desc', models.CharField(max_length=1000)),
                ('sop', models.FileField(upload_to='documents/SOP/')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('applicable_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.productmodel')),
            ],
        ),
        migrations.CreateModel(
            name='DroneConfigration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Drone_base_version', models.CharField(max_length=20)),
                ('CC_base_version', models.CharField(max_length=20)),
                ('FCS_base_version', models.CharField(max_length=20)),
                ('BLL_base_version', models.CharField(max_length=20)),
                ('drone_current_version', models.CharField(max_length=20)),
                ('CC_current_version', models.CharField(max_length=20)),
                ('FCS_current_version', models.CharField(max_length=20)),
                ('BLL_current_version', models.CharField(max_length=20)),
                ('Latest_version_available', models.CharField(max_length=20)),
                ('CC_Latest_version_available', models.CharField(max_length=20)),
                ('FCS_Latest_version_available', models.CharField(max_length=20)),
                ('BLL_Latest_version_available', models.CharField(max_length=20)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('drone_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.drone')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('District_name', models.CharField(max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.country')),
                ('state_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.state')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.district'),
        ),
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.state'),
        ),
        migrations.AddField(
            model_name='allocatedcustomer',
            name='AllocatedCustomer_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.country'),
        ),
        migrations.AddField(
            model_name='allocatedcustomer',
            name='AllocatedCustomer_district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.district'),
        ),
        migrations.AddField(
            model_name='allocatedcustomer',
            name='AllocatedCustomer_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.state'),
        ),
        migrations.AddField(
            model_name='allocatedcustomer',
            name='primary_customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customer'),
        ),
    ]
