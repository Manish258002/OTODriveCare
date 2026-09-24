from django.db import models
from accounts.models import User
from providers.models import Provider
from services.models import SERVICE_TYPES

VEHICLE_TYPES = [
    ('car', 'Car'),
    ('bike', 'Bike / Motorcycle'),
    ('truck', 'Truck'),
    ('auto', 'Auto Rickshaw'),
    ('bus', 'Bus'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('On the way', 'On the way'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]

PAYMENT_CHOICES = [
    ('Cash', 'Cash'),
    ('Online', 'Online'),
    ('Pending', 'Pending'),
]


class EmergencyRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_requests')
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_requests')
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, default='tire')
    from_location = models.CharField(max_length=200, blank=True, default='')
    to_location = models.CharField(max_length=200, blank=True, default='')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    description = models.TextField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    destination_latitude = models.FloatField(default=0.0)
    destination_longitude = models.FloatField(default=0.0)
    photo = models.ImageField(upload_to='breakdowns/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    confirmation_code = models.CharField(max_length=10, blank=True, default='')
    code_verified = models.BooleanField(default=False)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    payment_completed = models.BooleanField(default=False)
    rider_latitude = models.FloatField(default=0.0)
    rider_longitude = models.FloatField(default=0.0)
    request_time = models.DateTimeField(auto_now_add=True)
    accepted_time = models.DateTimeField(null=True, blank=True)
    completed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request #{self.pk} - {self.user.username} ({self.status})"

    class Meta:
        ordering = ['-request_time']
