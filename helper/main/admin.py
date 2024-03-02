from django.contrib import admin
from .models import Category, AddItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'created_on')


class AddItemAdmin(admin.ModelAdmin):
    list_display = ('Partname', 'Partcode', 'Version', 'created_on')


admin.site.register(Category, CategoryAdmin)
admin.site.register(AddItem, AddItemAdmin)
