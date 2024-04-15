from django.contrib import admin
from .models import Category, AddItem
from .models import ProductModel, Product, Warranty, ECN, Drone, Customer, AllocatedCustomer
from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'created_on')


class AddItemAdmin(admin.ModelAdmin):
    list_display = ('Partname', 'Partcode', 'Version', 'created_on')


admin.site.register(Category, CategoryAdmin)
admin.site.register(AddItem, AddItemAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'spec', 'description', 'created_on']


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'model_name', 'product', 'image', 'spec', 'description', 'created_on']


@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = ['id', 'primary_owner', 'secondry_owner', 'product', 'product_model', 'drone', 'dispatch_date',
                    'delivery_date', 'start_date', 'end_date', 'dispatch_list', 'handover_doc', 'created_on']


@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ['id', 'Drone_id', 'drone_type', 'UIN', 'AVB', 'created_on']


@admin.register(ECN)
class ECNAdmin(admin.ModelAdmin):
    list_display = ['id', 'release', 'expertise', 'applicable_on', 'type', 'name', 'department',
                    'release_by', 'release_date', 'desc', 'sop', 'created_on']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'address', 'city', 'district', 'state', 'country', 'pincode',
                    'contact', 'email', 'Escalation_contact', 'Escalation_email']


@admin.register(AllocatedCustomer)
class AllocatedCustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'primary_customer', 'AllocatedCustomer_name', 'AllocatedCustomer_address', 'AllocatedCustomer_city', 'AllocatedCustomer_country', 'AllocatedCustomer_state',
                    'AllocatedCustomer_district', 'AllocatedCustomer_pincode', 'AllocatedCustomer_contact', 'AllocatedCustomer_email', 'AllocatedCustomer_Escalation_contact', 'AllocatedCustomer_Escalation_email']
