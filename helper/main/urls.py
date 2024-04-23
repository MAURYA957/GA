from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetDoneView, PasswordResetView,
    PasswordResetCompleteView, PasswordResetConfirmView,
    PasswordChangeView, PasswordChangeDoneView
)
from .views import dashboard, success_view, register, ECN, Subscription, create_warranty, create_allocated_customer, \
    create_Drone, Warranty_data, create_sop, \
    view_config, update_config, Add_data, create_drone_configuration, \
    update_Trimble_data, download_handover_doc, download_dispatch_list, sop_list, productmodel_spec_view, \
    view_sop_document, download_sop_document
from . import views

app_name = 'authapp'

urlpatterns = [
                  path('dashboard/', dashboard, name='dashboard'),
                  path('register/', register, name='register'),
                  path('success/', views.success_view, name='success'),

                  # Warranty page Urls
                  path('download_handover_doc/<int:warranty_id>/', views.download_handover_doc,
                       name='download_handover_doc'),
                  path('download_dispatch_list/<int:warranty_id>/', views.download_dispatch_list,
                       name='download_dispatch_list'),
                  path('warranty_data/', views.Warranty_data, name='warranty_data'),
                  path('warranty/', views.create_warranty, name='warranty'),
                  # path('edit/', edit, name='edit'),
                  # SOP page urls
                  path('create_sop/', views.create_sop, name='create_sop'),
                  path('sop_list/', views.sop_list, name='sop_list'),
                  path('sop/<slug:slug>/download/', views.download_sop_document, name='download_sop_document'),
                  path('sop/<slug:slug>/', views.view_sop_document, name='view_sop_document'),
                  # path('productmodel/<int:pk>/spec/', views.productmodel_spec_view, name='productmodel_spec_view'),
                  # Config page urls
                  path('create_config/', views.create_drone_configuration, name='create_config'),
                  path('ecn_board/', views.view_config, name='ecn_board'),
                  path('update_config/<int:config_id>/', update_config, name='update_config'),
                  path('data/', views.Add_data, name='data'),
                  # Subscription url
                  path('subscription/', views.Subscription, name='subscription'),
                  path('update_subs/<int:id>/', views.update_Trimble_data, name='update_Trimble_data'),
                  path('drone_form/', views.create_Drone, name='drone_form'),
                  path('customer_form/', views.create_allocated_customer, name='customer_form'),

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
                  # path('product-model/<int:model_id>/image/', views.product_model_image, name='product-model-image'),

                  # URL pattern to serve product model specification file
                  # path('product-model/<int:model_id>/spec/', views.product_model_spec, name='product-model-spec'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
