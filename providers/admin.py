from django.contrib import admin
from .models import Provider


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'owner', 'address', 'rating', 'verified', 'is_available']
    list_filter = ['verified', 'is_available']
    search_fields = ['shop_name', 'address', 'owner__username']
    list_editable = ['verified', 'is_available']
    actions = ['verify_providers', 'unverify_providers']

    def verify_providers(self, request, queryset):
        queryset.update(verified=True)
    verify_providers.short_description = "Verify selected providers"

    def unverify_providers(self, request, queryset):
        queryset.update(verified=False)
    unverify_providers.short_description = "Unverify selected providers"
