from django.contrib.auth.models import User
from django import forms
from django.db import models
from datetime import timedelta
import requests
from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import fetch_countries_from_api


# from .models import Profile


class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='users/%Y/%M', blank=True)

    def __str__(self):
        return self.title


class AddItem(models.Model):
    Partname = models.CharField(max_length=200, unique=True)
    Partcode = models.CharField(max_length=100, unique=True)
    Version = models.CharField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='users/%Y/%M', blank=True)


# warranties/models.py
from django.db import models

expertise_choice = (
    ("1", "None"),
    ("2", "Pilot"),
    ("3", "Technician"),
    ("4", "Ops_Engineer"),
    ("5", "Support_agent"),
    ("6", "Developers")
)

State = (
    ("1", "Andhra Pradesh"),
    ("2", "Arunachal Pradesh"),
    ("3", "Assam"),
    ("4", "Bihar"),
    ("5", "Chhattisgarh"),
    ("6", "Goa"),
    ("7", "Gujarat"),
    ("8", "Haryana"),
    ("9", "Himachal Pradesh"),
    ("10", "Jharkhand"),
    ("11", "Karnataka"),
    ("12", "Kerala"),
    ("13", "Madhya Pradesh"),
    ("14", "Maharashtra"),
    ("15", "Manipur"),
    ("16", "Meghalaya"),
    ("17", "Mizoram"),
    ("18", "Nagaland"),
    ("19", "Odisha"),
    ("20", "Punjab"),
    ("21", "Rajasthan"),
    ("22", "Sikkim"),
    ("23", "Tamil Nadu"),
    ("24", "Telangana"),
    ("25", "Tripura"),
    ("26", "Uttar Pradesh"),
    ("27", "Uttarakhand"),
    ("28", "West Bengal"),

)

department_choice = (
    ("1", "None"),
    ("2", "Planner"),
    ("3", "Embedded"),
    ("4", "Ga_app"),
    ("5", "FCS"),
    ("6", "Hardware"),
    ("7", "Other")
)

type_choice = (
    ("1", "None"),
    ("2", "Software"),
    ("3", "Hardware"),
    ("4", "QC"),
    ("5", "Others")
)

type_drone = (
    ("1", "None"),
    ("2", "Service"),
    ("3", "Sold"),
    ("4", "Training"),
    ("5", "Others")
)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/media/image/product/', height_field=None, width_field=None,
                              max_length=100)
    spec = models.FileField(upload_to='static/documents/product/')
    description = models.TextField()
    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/media/image/model/', height_field=None, width_field=None,
                              max_length=100)
    spec = models.FileField(upload_to='static/documents/product/')
    description = models.TextField()
    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.model_name


class Drone(models.Model):
    id = models.AutoField(primary_key=True)
    Drone_id = models.CharField(max_length=20, unique=True)
    UIN = models.CharField(max_length=20, unique=True)
    drone_type = models.CharField(max_length=20, choices=type_drone, default=1)
    AVB = models.CharField(max_length=20)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Drone_id


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=100, choices=fetch_countries_from_api(), default='',
                               verbose_name=_('Country'))
    # state = models.CharField(max_length=100, choices=fetch_states_from_api(''), default='', verbose_name=_('State'))
    # district = models.CharField(max_length=100, choices=fetch_districts_from_api('', ''), default='',
    #                            verbose_name=_('District'))
    state = models.CharField(max_length=50, choices=State, default=1)
    district = models.CharField(max_length=20)
    pincode = models.IntegerField()
    contact = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    Escalation_contact = models.CharField(max_length=20)
    Escalation_email = models.EmailField(max_length=100)

    def __str__(self):
        return self.customer_name


class AllocatedCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    primary_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    AllocatedCustomer_name = models.CharField(max_length=20)
    AllocatedCustomer_country = models.CharField(max_length=100, choices=fetch_countries_from_api(), default='',
                                                 verbose_name=_('Country'))
    # AllocatedCustomer_state = models.CharField(max_length=100, choices=fetch_states_from_api(''), default='',
    #  verbose_name=_('State'))
    # AllocatedCustomer_district = models.CharField(max_length=100, choices=fetch_districts_from_api('', ''), default='',
    #  verbose_name=_('District'))
    AllocatedCustomer_state = models.CharField(max_length=50, choices=State, default=1)
    AllocatedCustomer_district = models.CharField(max_length=20)
    AllocatedCustomer_city = models.CharField(max_length=20)
    AllocatedCustomer_address = models.CharField(max_length=100)
    AllocatedCustomer_pincode = models.IntegerField()
    AllocatedCustomer_contact = models.CharField(max_length=20)
    AllocatedCustomer_email = models.EmailField(max_length=100)
    AllocatedCustomer_Escalation_contact = models.CharField(max_length=20)
    AllocatedCustomer_Escalation_email = models.EmailField(max_length=100)

    def __str__(self):
        return str(self.AllocatedCustomer_name)


class Warranty(models.Model):
    id = models.AutoField(primary_key=True)
    primary_owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    secondry_owner = models.ForeignKey(AllocatedCustomer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_model = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    dispatch_date = models.DateField()
    delivery_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    dispatch_list = models.FileField(upload_to='static/documents/dispatch/')
    handover_doc = models.FileField(upload_to='static/documents/handover/')
    created_on = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.end_date:  # If next_date is not already set
            self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.secondry_owner)

    def get_dispatch_list_url(self):
        return self.dispatch_list.url

    def get_handover_doc_url(self):
        return self.handover_doc.url


class ECN(models.Model):
    id = models.AutoField(primary_key=True)
    release = models.CharField(max_length=100)
    expertise = models.CharField(max_length=10, choices=expertise_choice, default=1)
    applicable_on = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=type_choice, default=1)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=department_choice, default=1)
    release_by = models.CharField(max_length=100)
    release_date = models.DateField()
    desc = models.CharField(max_length=1000)
    sop = models.FileField(upload_to='static/documents/SOP/')
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.release
