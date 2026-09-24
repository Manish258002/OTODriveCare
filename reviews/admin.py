from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'rating', 'date']
    list_filter = ['rating']
    search_fields = ['user__username', 'provider__shop_name', 'review']
    readonly_fields = ['date']
