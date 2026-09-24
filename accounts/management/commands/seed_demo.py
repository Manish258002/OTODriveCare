from datetime import time

from django.core.management.base import BaseCommand

from accounts.models import User
from providers.models import Provider
from services.models import Service, SERVICE_CATALOG


class Command(BaseCommand):
    help = 'Create admin, demo user, demo rider and catalog services'

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username='manish', defaults={
            'email': 'admin@otodrivecare.com',
            'is_staff': True,
            'is_superuser': True,
        })
        admin.set_password('manish2412')
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.save()

        user, _ = User.objects.get_or_create(username='user1', defaults={
            'email': 'user1@otodrivecare.com',
            'phone': '9876543210',
        })
        user.set_password('User@123')
        user.is_active = True
        user.save()

        rider, _ = User.objects.get_or_create(username='rider1', defaults={
            'email': 'rider1@otodrivecare.com',
            'phone': '9123456780',
            'is_rider': True,
            'is_provider': True,
            'on_duty': True,
            'location': 'Ahmedabad',
        })
        rider.set_password('Rider@123')
        rider.is_rider = True
        rider.is_provider = True
        rider.on_duty = True
        rider.is_active = True
        rider.save()

        provider, _ = Provider.objects.get_or_create(owner=rider, defaults={
            'shop_name': 'Rider1 Technician',
            'phone': rider.phone,
            'email': rider.email,
            'address': 'Ahmedabad roadside unit',
            'latitude': 23.0225,
            'longitude': 72.5714,
            'opening_time': time(0, 0),
            'closing_time': time(23, 59),
            'verified': True,
            'is_available': True,
        })
        provider.verified = True
        provider.is_available = True
        provider.save()

        for item in SERVICE_CATALOG:
            Service.objects.get_or_create(
                provider=provider,
                service_type=item['key'],
                defaults={
                    'service_name': item['name'],
                    'price': item['price'],
                    'description': item['desc'],
                    'is_active': True,
                },
            )

        self.stdout.write(self.style.SUCCESS('Demo accounts ready.'))
        self.stdout.write('Admin: manish / manish2412')
        self.stdout.write('User:  user1 / User@123')
        self.stdout.write('Rider: rider1 / Rider@123')
