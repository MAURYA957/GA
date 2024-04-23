from wsgiref.util import FileWrapper
from celery import shared_task
from celery.utils.time import timezone
from django.conf import settings
from django.contrib import messages
from django.http import request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Warranty, Product, Drone, AllocatedCustomer, ECN, User, DroneConfiguration, SOP
import os
from .forms import WarrantyForm, AllocatedCustomerForm, DroneForm, ProductModel, UserRegistrationForm, SOPForm, \
    Update_Config_Form, DroneConfigurationForm
from .forms import DroneConfigurationForm, update_Trimble_data_form
from datetime import datetime, timedelta
from .tasks import send_warranty_expiry_reminder


# Create your views here.

# Subscription page veiw codes

def Subscription(request):
    drones = Drone.objects.all()
    today = datetime.now().date()  # Get today's date
    for drone in drones:
        # Calculate subscription status
        if drone.Subscription_end_date < today:
            drone.subscription_status = 'Expired'
        else:
            days_remaining = (drone.Subscription_end_date - today).days
            drone.subscription_status = f'Active for next {days_remaining} days'
    return render(request, 'Subscription.html', {'drones': drones, 'today': today})


def update_Trimble_data(request, id):  # Add the 'id' parameter
    drone = get_object_or_404(Drone, id=id)  # Retrieve the drone object based on the id
    if request.method == 'POST':
        form = update_Trimble_data_form(request.POST, instance=drone)
        if form.is_valid():
            form.save()
            return render(request, 'Subscription.html.html')
            # Redirect to a success page or render a template
    else:
        form = update_Trimble_data_form(instance=drone)
    return render(request, 'update_subs.html', {'form': form})


""""@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'edit.html', context=context)"""


# Warranty page codes and subcodes

def Warranty_data(request):
    warranties = Warranty.objects.all()
    today = datetime.now().date()  # Get today's date
    for warranty in warranties:
        # Calculate subscription status
        if warranty.end_date < today:
            warranty.status = 'Expired'
        else:
            days_remaining = (warranty.end_date - today).days
            warranty.status = f'Active for next {days_remaining} days'
    return render(request, 'warranty_data.html', {'warranties': warranties, 'today': today})


def create_warranty(request):
    if request.method == 'POST':
        form = WarrantyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Warranty created successfully! Add new warranty')
            return render(request, 'warranty.html')
    else:
        form = WarrantyForm()
    return render(request, 'warranty.html', {'form': form})


def download_handover_doc(request, warranty_id):
    warranty = get_object_or_404(Warranty, id=warranty_id)
    handover_doc_path = warranty.handover_doc.path
    if os.path.exists(handover_doc_path):
        with open(handover_doc_path, 'rb') as file:
            response = HttpResponse(FileWrapper(file), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(warranty.handover_doc.name)
            return response
    else:
        return HttpResponse("File not found", status=404)


def download_dispatch_list(request, warranty_id):
    warranty = get_object_or_404(Warranty, id=warranty_id)
    dispatch_list_path = warranty.dispatch_list.path
    if os.path.exists(dispatch_list_path):
        with open(dispatch_list_path, 'rb') as file:
            response = HttpResponse(FileWrapper(file), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(warranty.dispatch_list.name)
            return response
    else:
        return HttpResponse("File not found", status=404)


@shared_task
def schedule_warranty_expiry_reminders():
    today = timezone.now().date()
    twenty_days_from_today = today + timedelta(days=20)
    ten_days_from_today = today + timedelta(days=10)
    zero_days_from_today = today
    twenty_days_left = twenty_days_from_today - today
    ten_days_left = ten_days_from_today - today
    zero_days_left = zero_days_from_today - today

    # Assuming you have AllocatedCustomer objects with their emails stored in a variable named allocated_customers
    for allocatedCustomer in AllocatedCustomer:
        send_warranty_expiry_reminder.apply_async(
            args=[allocatedCustomer.AllocatedCustomer_email, twenty_days_left.days], eta=twenty_days_from_today)
        send_warranty_expiry_reminder.apply_async(args=[allocatedCustomer.AllocatedCustomer_email, ten_days_left.days],
                                                  eta=ten_days_from_today)
        send_warranty_expiry_reminder.apply_async(args=[allocatedCustomer.AllocatedCustomer_email, zero_days_left.days],
                                                  eta=zero_days_from_today)


# Others view codes

def create_allocated_customer(request):
    if request.method == 'POST':
        form = AllocatedCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!, Add New Customer')
            return render(request, 'customer_form.html')
    else:
        form = AllocatedCustomerForm()
    return render(request, 'customer_form.html', {'form': form})


def create_Drone(request):
    if request.method == 'POST':
        form = DroneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drone created successfully! Add new Drone')
            return render(request, 'drone_form.html')
    else:
        form = DroneForm()
    return render(request, 'drone_form.html', {'form': form})


# Main dashboard view code
@login_required
def dashboard(request):
    productmodels = ProductModel.objects.all()
    return render(request, 'dashboard.html', {'productmodels': productmodels})


def productmodel_spec_view(request, pk):
    # Retrieve the ProductModel instance
    productmodel = get_object_or_404(ProductModel, pk=pk)

    # Open the PDF file and read its content
    with open(productmodel.spec.path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    # Set the appropriate content type for PDF files
    response = HttpResponse(pdf_content, content_type='application/pdf')

    # Set the Content-Disposition header to force the file download
    response['Content-Disposition'] = f'attachment; filename="{productmodel.model_name}_spec.pdf"'

    return response


def success_view(request):
    return render(request, 'success.html')  # Assuming you have a template named 'success.html'


def Add_data(request):
    return render(request, 'data.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')  # Redirect to a success page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Config view codes

def view_config(request):
    drone_configurations = DroneConfiguration.objects.all()
    return render(request, 'ecn_board.html', {'drone_configurations': drone_configurations})


def update_config(request, config_id):
    print("Inside update_config view function")
    config = get_object_or_404(DroneConfiguration, pk=config_id)
    if request.method == 'POST':
        print("Request method is POST")
        form = Update_Config_Form(request.POST, instance=config)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, 'Configuration updated successfully.')
            return render('ecn_board')  # Redirect to the ECN board page after successful update
        else:
            print("Form has errors:", form.errors)
    else:
        form = Update_Config_Form(instance=config)
    return render(request, 'update_config.html', {'form': form})


def create_drone_configuration(request):
    if request.method == 'POST':
        form = DroneConfigurationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or do any other processing
            return redirect(
                'authapp:ecn_board')  # Replace 'success_page' with the name of your success page URL pattern
    else:
        form = DroneConfigurationForm()
    return render(request, 'create_config.html', {'form': form})


# Sop page code

def create_sop(request):
    if request.method == 'POST':
        form = SOPForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Display success message
            messages.success(request, 'SOP created successfully!')
            # Redirect to a success page or do something else
            return redirect('create_sop')  # Assuming you have a URL pattern named 'home' for the home page
    else:
        form = SOPForm()
    return render(request, 'create_sop.html', {'form': form})


def sop_list(request):
    sops = SOP.objects.all()
    return render(request, 'sop_list.html', {'sops': sops})


def view_sop_document(request, slug):
    sop = get_object_or_404(SOP, slug=slug)
    return render(request, 'sop_document.html', {'sop': sop})


def download_sop_document(request, slug):
    sop = get_object_or_404(SOP, slug=slug)
    sop_file = sop.document.path
    response = HttpResponse(open(sop_file, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{sop.name}.pdf"'
    return response
