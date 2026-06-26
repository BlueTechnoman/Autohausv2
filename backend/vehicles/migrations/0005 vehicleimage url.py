from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0004_vehicle_extra_fields_pricehistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicleimage',
            name='image',
        ),
        migrations.AddField(
            model_name='vehicleimage',
            name='image_url',
            field=models.URLField(
                max_length=500,
                verbose_name='Bild-URL',
                default='',
            ),
            preserve_default=False,
        ),
    ]