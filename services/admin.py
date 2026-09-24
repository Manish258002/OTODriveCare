from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_type', 'provider', 'price', 'is_active']
    list_filter = ['service_type', 'is_active']
    search_fields = ['service_name', 'provider__shop_name']
    list_editable = ['is_active']
