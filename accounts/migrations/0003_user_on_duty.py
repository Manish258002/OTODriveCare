from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_rider'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='on_duty',
            field=models.BooleanField(default=False),
        ),
    ]
