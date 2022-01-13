from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackendCode', 'ProductImage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='/placeholder.png', null=True, upload_to=''),
        ),
    ]
