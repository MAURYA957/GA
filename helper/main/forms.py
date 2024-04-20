from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Warranty, Customer, AllocatedCustomer, Product, ProductModel, Drone, Country, State, District, \
    DroneConfigration, ECN
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from .models import User
from tinymce.widgets import TinyMCE


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'contact_no', 'user_mail', 'user_type', 'country', 'state_name', 'district', 'user_profile',
                  'password']

    def clean_contact_no(self):
        contact_no = self.cleaned_data['contact_no']
        if not contact_no.isdigit():  # Check if contact number contains only digits
            raise forms.ValidationError("Contact number should contain only digits.")
        return contact_no

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return make_password(password)  # Hash the password for security


class WarrantyForm(forms.ModelForm):
    primary_owner = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Primary Owner'}))
    secondry_owner = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Secondary Owner'}))
    product = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Product'}))
    product_model = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Product Model'}))
    drone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Drone'}))
    dispatch_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Dispatch Date'}))
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Delivery Date'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Start Date'}))
    dispatch_list = forms.FileField(widget=forms.FileInput(attrs={'placeholder': 'Dispatch List'}))
    handover_doc = forms.FileField(widget=forms.FileInput(attrs={'placeholder': 'Handover Document'}))

    class Meta:
        model = Warranty
        fields = ['primary_owner', 'secondry_owner', 'product', 'product_model', 'drone',
                  'dispatch_date', 'delivery_date', 'start_date', 'end_date', 'dispatch_list', 'handover_doc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'] = forms.ModelChoiceField(
            queryset=AllocatedCustomer.objects.values_list('AllocatedCustomer_city', flat=True).distinct(),
            required=True,
            widget=forms.Select(attrs={'placeholder': 'City'})
        )
        self.fields['uin'] = forms.ModelChoiceField(
            queryset=Drone.objects.values_list('UIN', flat=True).distinct(),
            required=True,
            widget=forms.Select(attrs={'placeholder': 'UIN'})
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        if start_date:
            end_date = start_date + timedelta(days=365)  # Add one year
            cleaned_data["end_date"] = end_date
        return cleaned_data



class AllocatedCustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AllocatedCustomerForm, self).__init__(*args, **kwargs)

        # Add CSS classes and placeholders for each field
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': f'Enter {field.label}'})

        # Add JavaScript for dynamic selection
        self.fields['AllocatedCustomer_country'].widget.attrs.update({'onchange': 'selectState(this.value)'})
        self.fields['AllocatedCustomer_state'].widget.attrs.update({'onchange': 'selectDistrict(this.value)'})

    class Meta:
        model = AllocatedCustomer
        fields = ['primary_customer', 'AllocatedCustomer_name', 'AllocatedCustomer_country',
                  'AllocatedCustomer_state', 'AllocatedCustomer_district', 'AllocatedCustomer_city',
                  'AllocatedCustomer_address', 'AllocatedCustomer_pincode', 'AllocatedCustomer_contact',
                  'AllocatedCustomer_email', 'AllocatedCustomer_Escalation_contact',
                  'AllocatedCustomer_Escalation_email']
        widgets = {
            'AllocatedCustomer_country': forms.Select(attrs={'class': 'form-control country-select'}),
            'AllocatedCustomer_state': forms.Select(attrs={'class': 'form-control state-select'}),
            'AllocatedCustomer_district': forms.Select(attrs={'class': 'form-control district-select'}),
        }


class DroneForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ['Drone_id', 'UIN', 'drone_type', 'AVB', 'Timble_module', 'Subscription_date', 'Subscription_end_date',
                  'Drone_base_version', 'CC_base_version', 'FCS_base_version', 'BLL_base_version']
        widgets = {
            'Drone_id': forms.TextInput(attrs={'placeholder': 'Enter Drone ID', 'class': 'form-control'}),
            'UIN': forms.TextInput(attrs={'placeholder': 'Enter UIN', 'class': 'form-control'}),
            'drone_type': forms.TextInput(attrs={'placeholder': 'Enter Drone Type', 'class': 'form-control'}),
            'AVB': forms.TextInput(attrs={'placeholder': 'Enter AVB', 'class': 'form-control'}),
            'Timble_module': forms.TextInput(attrs={'placeholder': 'Enter Timble Module', 'class': 'form-control'}),
            'Subscription_date': forms.DateInput(attrs={'placeholder': 'Enter Subscription Date', 'class': 'form-control'}),
            'Subscription_end_date': forms.DateInput(attrs={'placeholder': 'Enter Subscription End Date', 'class': 'form-control'}),
            'Drone_base_version': forms.TextInput(attrs={'placeholder': 'Enter Drone Base Version', 'class': 'form-control'}),
            'CC_base_version': forms.TextInput(attrs={'placeholder': 'Enter CC Base Version', 'class': 'form-control'}),
            'FCS_base_version': forms.TextInput(attrs={'placeholder': 'Enter FCS Base Version', 'class': 'form-control'}),
            'BLL_base_version': forms.TextInput(attrs={'placeholder': 'Enter BLL Base Version', 'class': 'form-control'}),
        }


from django import forms
from .models import DroneConfigration, ECN


class DroneConfigrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DroneConfigrationForm, self).__init__(*args, **kwargs)

        # Add CSS classes and placeholders for each field
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': f'Enter {field.label}'})

        # Retrieve unique values for each field
        self.fields['drone_current_version'].queryset = ECN.objects.values_list('Drone_version', flat=True).distinct()
        self.fields['CC_current_version'].queryset = ECN.objects.values_list('CC_version', flat=True).distinct()
        self.fields['FCS_current_version'].queryset = ECN.objects.values_list('FCS_version', flat=True).distinct()
        self.fields['BLL_current_version'].queryset = ECN.objects.values_list('BLL_version', flat=True).distinct()

    class Meta:
        model = DroneConfigration
        fields = ['drone_id', 'drone_current_version', 'CC_current_version', 'FCS_current_version',
                  'BLL_current_version']


class SOPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SOPForm, self).__init__(*args, **kwargs)

        # Add CSS classes and placeholders for each field
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': f'Enter {field.label}'})

    class Meta:
        model = SOP
        fields = ['name', 'slug', 'user_types', 'drone_model', 'sop_type', 'desc', 'document']
        widgets = {
            'desc': TinyMCE(attrs={'cols': 80, 'rows': 20}),  # Use TinyMCE for desc field
        }

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional cleaning logic here if needed
        return cleaned_data
