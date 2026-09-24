from django.contrib import admin
from .models import EmergencyRequest


@admin.register(EmergencyRequest)
class EmergencyRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'provider', 'vehicle_type', 'status', 'request_time']
    list_filter = ['status', 'vehicle_type']
    search_fields = ['user__username', 'provider__shop_name']
    readonly_fields = ['request_time', 'accepted_time', 'completed_time']
