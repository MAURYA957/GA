from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Warranty, Customer, AllocatedCustomer, Product, ProductModel, Drone, Country, State, District, \
    DroneConfigration, ECN
from datetime import timedelta


class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


"""class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ['primary_owner', 'secondry_owner', 'product', 'product_model', 'drone',
                  'dispatch_date', 'delivery_date', 'start_date', 'end_date', 'dispatch_list', 'handover_doc']
        widgets = {
            'dispatch_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }"""


class WarrantyForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=AllocatedCustomer.objects.values_list('AllocatedCustomer_city', flat=True).distinct(), required=True)
    uin = forms.ModelChoiceField(queryset=Drone.objects.values_list('UIN', flat=True).distinct(), required=True)

    class Meta:
        model = Warranty
        fields = ['primary_owner', 'secondry_owner', 'product', 'product_model', 'drone',
                  'dispatch_date', 'delivery_date', 'start_date', 'end_date', 'dispatch_list', 'handover_doc']
        widgets = {
            'dispatch_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        if start_date:
            end_date = start_date + timedelta(days=365)  # Add one year
            cleaned_data["end_date"] = end_date
        return cleaned_data


class AllocatedCustomerForm(forms.ModelForm):
    class Meta:
        model = AllocatedCustomer
        fields = ['primary_customer', 'AllocatedCustomer_name', 'AllocatedCustomer_country',
                  'AllocatedCustomer_state', 'AllocatedCustomer_district', 'AllocatedCustomer_city',
                  'AllocatedCustomer_address', 'AllocatedCustomer_pincode', 'AllocatedCustomer_contact',
                  'AllocatedCustomer_email', 'AllocatedCustomer_Escalation_contact',
                  'AllocatedCustomer_Escalation_email']
        widgets = {
            'AllocatedCustomer_country': forms.Select(attrs={'class': 'country-select'}),
            'AllocatedCustomer_state': forms.Select(attrs={'class': 'state-select'}),
            'AllocatedCustomer_district': forms.Select(attrs={'class': 'district-select'}),
        }


class DroneForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ['Drone_id', 'UIN', 'drone_type', 'AVB', 'Timble_module', 'Subscription_date', 'Subscription_end_date',
                  'Drone_base_version', 'CC_base_version', 'FCS_base_version', 'BLL_base_version']


class DroneConfigrationForm(forms.ModelForm):
    class Meta:
        model = DroneConfigration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any additional customization to form fields here if needed
