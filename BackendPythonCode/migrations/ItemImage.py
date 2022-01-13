from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackendCode', 'OrderItemShippingAddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
