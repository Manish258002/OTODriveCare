from django.db import models
from accounts.models import User


class Provider(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    shop_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    rating = models.FloatField(default=0.0)
    verified = models.BooleanField(default=False)
    shop_image = models.ImageField(upload_to='shops/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name

    class Meta:
        ordering = ['-rating']
