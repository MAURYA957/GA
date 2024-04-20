from django.conf import settings
from django.contrib import messages
from django.http import request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Warranty, Product, Drone, AllocatedCustomer, ECN, User, DroneConfiguration
from django.http import FileResponse
import os
from .forms import WarrantyForm, AllocatedCustomerForm, DroneForm, ProductModel, UserRegistrationForm, SOPForm, updateConfigurationForm, DroneConfigurationForm
from .forms import DroneConfigurationForm, DroneUpdateForm


# Create your views here.

def Subscription(request):
    drones = Drone.objects.all()
    return render(request, 'Subscription.html', {'drones': drones})

def update_drone(request, id):  # Add the 'id' parameter
    drone = get_object_or_404(Drone, id=id)  # Retrieve the drone object based on the id
    if request.method == 'POST':
        form = DroneUpdateForm(request.POST, instance=drone)
        if form.is_valid():
            form.save()
            return render(request, 'Subscription.html.html')
            # Redirect to a success page or render a template
    else:
        form = DroneUpdateForm(instance=drone)
    return render(request, 'update_subs.html', {'form': form})


def download_file(request, file_path):
    # Get the full file path
    full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    # Open the file for reading
    with open(full_file_path, 'rb') as file:
        response = FileResponse(file)
        # Set the content type for the response
        response['Content-Type'] = 'application/octet-stream'
        # Set the Content-Disposition header to force download
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(full_file_path)}"'
        return response


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')  # Redirect to a success page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


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


def Warranty_data(request):
    warranties = Warranty.objects.all()
    return render(request, 'warranty_data.html', {'warranties': warranties})


def product_model_image(request, model_id):
    product_model = get_object_or_404(ProductModel, pk=model_id)
    image_url = product_model.get_image_url()  # Assuming you have defined a get_image_url() method in your ProductModel model
    # Serve the image using HttpResponse
    return HttpResponse(image_url)


def product_model_spec(request, model_id):
    product_model = get_object_or_404(ProductModel, pk=model_id)
    spec_url = product_model.get_spec_url()  # Assuming you have defined a get_spec_url() method in your ProductModel model
    # Serve the file using HttpResponse
    return HttpResponse(spec_url)


@login_required
def dashboard(request):
    productmodels = ProductModel.objects.all()
    return render(request, 'dashboard.html', {'productmodels': productmodels})


def success_view(request):
    return render(request, 'success.html')  # Assuming you have a template named 'success.html'


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


def Add_data(request):
    return render(request, 'data.html')


def view_config(request):
    drone_configurations = DroneConfiguration.objects.all()
    return render(request, 'ecn_board.html', {'drone_configurations': drone_configurations})


def update_config(request, config_id):
    config = get_object_or_404(DroneConfiguration, pk=config_id)
    if request.method == 'POST':
        form = updateConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuration updated successfully.')
            # Redirect to the ECN board page after successful update
            return redirect('authapp:ecn_board')
    else:
        form = DroneConfigurationForm(instance=config)
    return render(request, 'update_config.html', {'form': form})


def create_drone_configuration(request):
    if request.method == 'POST':
        form = DroneConfigurationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or do any other processing
            return redirect('ecn_board')  # Replace 'success_page' with the name of your success page URL pattern
    else:
        form = DroneConfigurationForm()
    return render(request, 'create_config.html', {'form': form})