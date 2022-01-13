from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BackendCode', 'ReviewTimestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='timestamp',
        ),
    ]
