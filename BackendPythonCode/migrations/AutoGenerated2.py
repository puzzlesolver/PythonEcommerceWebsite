from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BackendCode', 'RemoveOrderTimestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
