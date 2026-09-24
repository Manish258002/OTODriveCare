from django.db import models
from accounts.models import User


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    reply_message = models.TextField(blank=True, default='')
    replied_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.email}'


class Complaint(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('rider', 'Service Provider'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    admin_reply = models.TextField(blank=True, default='')
    replied_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} ({self.user.username})'
