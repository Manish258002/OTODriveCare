from django.contrib import admin
from .models import ContactMessage, Complaint


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['subject', 'message', 'user__username']
    readonly_fields = ['user', 'role', 'subject', 'message', 'created_at']
