from django.db import models
from providers.models import Provider

SERVICE_TYPES = [
    ('towing', 'Towing'),
    ('battery', 'Battery'),
    ('tire', 'Tire'),
    ('fuel', 'Fuel'),
    ('oil_change', 'Oil Change'),
    ('jump_start', 'Jump Start'),
]

SERVICE_CATALOG = [
    {'key': 'towing', 'name': 'Towing', 'price': 1499, 'icon': 'fa-truck-pickup', 'color': 'danger', 'desc': 'Pickup a damaged vehicle and tow it safely.'},
    {'key': 'battery', 'name': 'Battery', 'price': 799, 'icon': 'fa-car-battery', 'color': 'warning', 'desc': 'On-spot battery check and replacement.'},
    {'key': 'tire', 'name': 'Tire', 'price': 499, 'icon': 'fa-circle-dot', 'color': 'primary', 'desc': 'Puncture repair and spare tire help.'},
    {'key': 'fuel', 'name': 'Fuel', 'price': 399, 'icon': 'fa-gas-pump', 'color': 'success', 'desc': 'Emergency petrol or diesel delivery.'},
    {'key': 'oil_change', 'name': 'Oil Change', 'price': 699, 'icon': 'fa-oil-can', 'color': 'info', 'desc': 'Mobile oil change for your vehicle.'},
    {'key': 'jump_start', 'name': 'Jump Start', 'price': 349, 'icon': 'fa-bolt', 'color': 'warning', 'desc': 'Jump start a dead battery quickly.'},
]


def catalog_price(service_type):
    for item in SERVICE_CATALOG:
        if item['key'] == service_type:
            return item['price']
    return 499


class Service(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, default='other')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service_name} - {self.provider.shop_name}"

    class Meta:
        ordering = ['service_name']
