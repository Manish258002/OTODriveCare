from django.db import migrations


def create_admin_user(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    if not User.objects.filter(username='manish').exists():
        User.objects.create_superuser(username='manish', password='manish2412', email='admin@otodrivecare.local')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, reverse_code=migrations.RunPython.noop),
    ]
