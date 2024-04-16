from django.contrib.auth.models import User
from django import forms
from datetime import timedelta
from django.db import models

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

expertise_choice = (
    ("1", "None"),
    ("2", "Pilot"),
    ("3", "Technician"),
    ("4", "Ops_Engineer"),
    ("5", "Support_agent"),
    ("6", "Developers")
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


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class State(models.Model):
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.state_name


class District(models.Model):
    id = models.AutoField(primary_key=True)
    District_name = models.CharField(max_length=100)
    state_name = models.ForeignKey(State, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.District_name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/product/', height_field=None, width_field=None,
                              max_length=100)
    spec = models.FileField(upload_to='documents/product/')
    description = models.TextField()
    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/productmodel/', height_field=None, width_field=None,
                              max_length=100)
    spec = models.FileField(upload_to='documents/productmodel/')
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


@classmethod
def get_uin_choices(cls):
    # Query the Drone model to get unique UIN values
    uins = Drone.objects.values_list('UIN', flat=True).distinct()
    # Convert the query result to a list of tuples for dropdown choices
    uin_choices = [(uin, uin) for uin in uins]
    return uin_choices


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
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
    AllocatedCustomer_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    AllocatedCustomer_state = models.ForeignKey(State, on_delete=models.CASCADE)
    AllocatedCustomer_district = models.ForeignKey(District, on_delete=models.CASCADE)
    AllocatedCustomer_city = models.CharField(max_length=20)
    AllocatedCustomer_address = models.CharField(max_length=100)
    AllocatedCustomer_pincode = models.IntegerField()
    AllocatedCustomer_contact = models.CharField(max_length=20)
    AllocatedCustomer_email = models.EmailField(max_length=100)
    AllocatedCustomer_Escalation_contact = models.CharField(max_length=20)
    AllocatedCustomer_Escalation_email = models.EmailField(max_length=100)

    def __str__(self):
        return str(self.AllocatedCustomer_name)


@classmethod
def get_city_choices(cls):
    # Query the AllocatedCustomer model to get unique city values
    cities = AllocatedCustomer.objects.values_list('AllocatedCustomer_city', flat=True).distinct()
    # Convert the query result to a list of tuples for dropdown choices
    city_choices = [(city, city) for city in cities]
    return city_choices


"""class Meta:
    verbose_name = _("Warranty")
    verbose_name_plural = _("Warranties")"""


class Warranty(models.Model):
    id = models.AutoField(primary_key=True)
    primary_owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    secondry_owner = models.ForeignKey(AllocatedCustomer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_model = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    #uin = models.CharField(max_length=100, choices=get_uin_choices, default=None)
    #city = models.CharField(max_length=100, choices=get_city_choices, default=None)
    dispatch_date = models.DateField()
    delivery_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    dispatch_list = models.FileField(upload_to='documents/dispatch/')
    handover_doc = models.FileField(upload_to='documents/handover/')
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
    sop = models.FileField(upload_to='documents/SOP/')
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.release
