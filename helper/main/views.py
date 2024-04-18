from django.conf import settings
from django.contrib import messages
from django.http import request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Warranty, Product, Drone, AllocatedCustomer, DroneConfigration
from django.http import FileResponse
import os
from .forms import WarrantyForm, AllocatedCustomerForm, DroneForm, DroneConfigrationForm, UserRegistration, \
    UserEditForm, ProductModel, DroneConfigrationForm


# Create your views here.


@login_required
def dashboard(request):
    productmodels = ProductModel.objects.all()
    return render(request, 'dashboard.html', {'productmodels': ProductModel})


def ECN(request):
    warranties = Warranty.objects.all()
    return render(request, 'ecn_board.html', {'warranties': warranties})


def Subscription(request):
    return render(request, 'subscription.html')


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
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'register.html', context=context)


@login_required
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
    return render(request, 'edit.html', context=context)


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


"""def update_config(request, config_id):
    config = DroneConfigration.objects.get(id=config_id)
    if request.method == 'POST':
        form = DroneConfigrationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drone config updated successfully!')
            return redirect('config-detail', config_id=config_id)  # Redirect to detail view
    else:
        form = DroneConfigrationForm(instance=config)
    return render(request, 'update_config.html', {'form': form})"""


def Warranty_data(request):
    return render(request, 'warranty_data.html')


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


def view_config(request):
    configurations = DroneConfigration.objects.all()  # Fetch all configurations
    return render(request, 'ecn_board.html', {'configurations': configurations})


def update_config(request, config_id):
    config = DroneConfigration.objects.get(id=config_id)

    if request.method == 'POST':
        form = DroneConfigrationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect('view_config')  # Redirect to the correct URL pattern name
    else:
        form = DroneConfigrationForm(instance=config)

    return render(request, 'update_config.html', {'form': form})
