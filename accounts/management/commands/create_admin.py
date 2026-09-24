from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create the admin user (manish / manish2412)'

    def handle(self, *args, **options):
        username = 'manish'
        password = 'manish2412'
        email = 'admin@otodrivecare.com'

        user, created = User.objects.get_or_create(username=username, defaults={
            'email': email,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        })
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.email = email
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" updated.'))
