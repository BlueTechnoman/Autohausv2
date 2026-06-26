# Generated manually – adds extra vehicle fields & PriceHistory model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_remove_vehicle_image_vehicleimage'),
    ]

    operations = [
        # ── Neue Felder am Vehicle-Model ──────────────────────────────
        migrations.AddField(
            model_name='vehicle',
            name='kraftstoff',
            field=models.CharField(
                choices=[
                    ('benzin',      'Benzin'),
                    ('diesel',      'Diesel'),
                    ('elektro',     'Elektro'),
                    ('hybrid',      'Hybrid'),
                    ('plug_in',     'Plug-in-Hybrid'),
                    ('lpg',         'Autogas (LPG)'),
                    ('erdgas',      'Erdgas (CNG)'),
                    ('wasserstoff', 'Wasserstoff'),
                    ('sonstige',    'Sonstige'),
                ],
                default='benzin',
                max_length=20,
                verbose_name='Kraftstoff',
            ),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='getriebe',
            field=models.CharField(
                choices=[
                    ('manuell',       'Schaltgetriebe'),
                    ('automatik',     'Automatik'),
                    ('halbautomatik', 'Halbautomatik'),
                ],
                default='manuell',
                max_length=20,
                verbose_name='Getriebe',
            ),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='leistung',
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name='Leistung (PS)',
            ),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='farbe',
            field=models.CharField(
                blank=True,
                default='',
                max_length=50,
                verbose_name='Farbe',
            ),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='ez',
            field=models.CharField(
                blank=True,
                default='',
                max_length=7,
                verbose_name='Erstzulassung',
            ),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='hu',
            field=models.CharField(
                blank=True,
                default='',
                max_length=7,
                verbose_name='HU bis',
            ),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='tueren',
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name='Türanzahl',
            ),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='beschreibung',
            field=models.TextField(
                blank=True,
                default='',
                verbose_name='Beschreibung',
            ),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='ausstattung',
            field=models.JSONField(
                blank=True,
                default=list,
                verbose_name='Ausstattung',
            ),
        ),

        # ── Neues PriceHistory-Model ──────────────────────────────────
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                )),
                ('price', models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name='Preis',
                )),
                ('recorded_at', models.DateField(
                    auto_now_add=True,
                    verbose_name='Datum',
                )),
                ('note', models.CharField(
                    blank=True,
                    default='',
                    max_length=255,
                    verbose_name='Notiz',
                )),
                ('vehicle', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='price_history',
                    to='vehicles.vehicle',
                )),
            ],
            options={
                'ordering': ['-recorded_at'],
            },
        ),
    ]