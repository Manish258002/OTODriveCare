from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='reply_message',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='replied_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
