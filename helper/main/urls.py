from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetDoneView, PasswordResetView,
    PasswordResetCompleteView, PasswordResetConfirmView,
    PasswordChangeView, PasswordChangeDoneView
)
from .views import dashboard, success_view, register, ECN, Subscription, create_warranty, create_allocated_customer, create_Drone, Warranty_data, product_model_spec, product_model_image, view_config, update_config
from . import views

app_name = 'authapp'

urlpatterns = [
    path('register/', register, name='register'),
    path('success/', views.success_view, name='success'),
    #path('edit/', edit, name='edit'),
    path('dashboard/', dashboard, name='dashboard'),
    path('warranty_data/', views.Warranty_data, name='warranty_data'),
    path('ecn_board/', views.view_config, name='ecn_board'),
    path('update_config/', views.update_config, name='update_config'),
    path('subscription/', views.Subscription, name='subscription'),
    #path('update_config/<int:config_id>/', views.update_config, name='update-config'),
    path('drone_form/', views.create_Drone, name='drone_form'),
    path('customer_form/', views.create_allocated_customer, name='customer_form'),
    path('warranty/', views.create_warranty, name='warranty'),
    path('download/<path:file_path>/', views.download_file, name='download_file'),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='password_change_form.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='authapp/password_change_done.html'),
        name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='authapp/password_reset_form.html',
        email_template_name='authapp/password_reset_email.html',
        success_url=reverse_lazy('authapp:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='authapp/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='authapp/password_reset_confirm.html',
        success_url=reverse_lazy('authapp:login')),
        name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='authapp/password_reset_complete.html'),
        name='password_reset_complete'),
    # URL pattern to serve product model image
    path('product-model/<int:model_id>/image/', views.product_model_image, name='product-model-image'),

    # URL pattern to serve product model specification file
    path('product-model/<int:model_id>/spec/', views.product_model_spec, name='product-model-spec'),


]
