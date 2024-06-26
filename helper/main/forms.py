from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Warranty, Customer, AllocatedCustomer, Product, ProductModel, Drone, Country, State, District, \
    DroneConfiguration, ECN
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from .models import User
from tinymce.widgets import TinyMCE
from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['name', 'contact_no', 'user_mail', 'user_type', 'country', 'state_name', 'district', 'user_profile',
                  'password']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'contact_no': forms.TextInput(attrs={'placeholder': 'Contact Number'}),
            'user_mail': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'user_type': forms.Select(attrs={'placeholder': 'User Type'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'state_name': forms.TextInput(attrs={'placeholder': 'State'}),
            'district': forms.TextInput(attrs={'placeholder': 'District'}),
            'user_profile': forms.FileInput(attrs={'placeholder': 'Profile Picture'}),
        }

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
    secondary_owner = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Secondary Owner'}))
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
        fields = ['primary_owner', 'secondary_owner', 'product', 'product_model', 'drone',
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
        fields = ['Drone_id', 'UIN', 'drone_type', 'AVB', 'Timble_module', 'Subscription_date', 'Subscription_end_date']
        widgets = {
            'Drone_id': forms.TextInput(attrs={'placeholder': 'Enter Drone ID', 'class': 'form-control'}),
            'UIN': forms.TextInput(attrs={'placeholder': 'Enter UIN', 'class': 'form-control'}),
            'drone_type': forms.Select(attrs={'class': 'form-control'}),  # Use forms.Select for dropdown
            'AVB': forms.TextInput(attrs={'placeholder': 'Enter AVB', 'class': 'form-control'}),
            'Timble_module': forms.TextInput(attrs={'placeholder': 'Enter Trimble Module', 'class': 'form-control'}),
            'Subscription_date': forms.DateInput(
                attrs={'placeholder': 'Enter Subscription Date', 'class': 'form-control'}),
            'Subscription_end_date': forms.DateInput(
                attrs={'placeholder': 'Enter Subscription End Date', 'class': 'form-control'}),
        }


class update_Trimble_data_form(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ['Timble_module', 'Subscription_date', 'Subscription_end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Timble_module'].widget.attrs['placeholder'] = 'Enter Trimble Module'

        # Add Bootstrap Datepicker for date fields
        datepicker_attrs = {
            'autocomplete': 'off',
            'placeholder': 'Select Date',
            'class': 'form-control datepicker',  # Add 'datepicker' class for Bootstrap Datepicker
        }
        self.fields['Subscription_date'].widget.attrs.update(datepicker_attrs)
        self.fields['Subscription_end_date'].widget.attrs.update(datepicker_attrs)


class Update_Config_Form(forms.ModelForm):
    drone_current_version = forms.CharField(max_length=20, label='Drone Current Version')
    CC_current_version = forms.CharField(max_length=20, label='CC Current Version')
    FCS_current_version = forms.CharField(max_length=20, label='FCS Current Version')
    BLL_current_version = forms.CharField(max_length=20, label='BLL Current Version')

    class Meta:
        model = DroneConfiguration
        fields = ['drone_current_version', 'CC_current_version', 'FCS_current_version', 'BLL_current_version']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


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


class DroneConfigurationForm(forms.ModelForm):
    class Meta:
        model = DroneConfiguration
        fields = '__all__'  # Use all fields from the model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Drone_base_version'].widget.attrs['placeholder'] = 'Drone Base Version'
        self.fields['CC_base_version'].widget.attrs['placeholder'] = 'CC Base Version'
        self.fields['FCS_base_version'].widget.attrs['placeholder'] = 'FCS Base Version'
        self.fields['BLL_base_version'].widget.attrs['placeholder'] = 'BLL Base Version'
        self.fields['drone_current_version'].widget.attrs['placeholder'] = 'Drone Current Version'
        self.fields['CC_current_version'].widget.attrs['placeholder'] = 'CC Current Version'
        self.fields['FCS_current_version'].widget.attrs['placeholder'] = 'FCS Current Version'
        self.fields['BLL_current_version'].widget.attrs['placeholder'] = 'BLL Current Version'


class ECNForm(forms.ModelForm):
    class Meta:
        model = ECN
        fields = ['release', 'Drone_version', 'CC_version', 'FCS_version', 'BLL_version', 'expertise',
                  'applicable_on', 'type', 'name', 'department', 'release_by', 'release_date', 'desc', 'sop']
        widgets = {
            'release': forms.TextInput(attrs={'placeholder': 'Release'}),
            'Drone_version': forms.TextInput(attrs={'placeholder': 'Drone Version'}),
            'CC_version': forms.TextInput(attrs={'placeholder': 'CC Version'}),
            'FCS_version': forms.TextInput(attrs={'placeholder': 'FCS Version'}),
            'BLL_version': forms.TextInput(attrs={'placeholder': 'BLL Version'}),
            'expertise': forms.Select(attrs={'placeholder': 'Expertise'}),
            'applicable_on': forms.Select(attrs={'placeholder': 'Applicable On'}),
            'type': forms.Select(attrs={'placeholder': 'Type'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'department': forms.Select(attrs={'placeholder': 'Department'}),
            'release_by': forms.TextInput(attrs={'placeholder': 'Release By'}),
            'release_date': forms.DateInput(attrs={'placeholder': 'Release Date'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Description'}),
            'sop': forms.FileInput(attrs={'placeholder': 'SOP Document'}),
        }