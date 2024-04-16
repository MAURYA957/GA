from django.conf import settings
from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm
from .models import Category, Warranty, Product, Drone, AllocatedCustomer
from django.http import FileResponse
import os


# Create your views here.


@login_required
def dashboard(request):
    warranties = Warranty.objects.all()
    return render(request, 'dashboard.html', {'warranties': warranties})


def ECN(request):
    warranties = Warranty.objects.all()
    return render(request, 'ecn_board.html', {'warranties': warranties})


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
