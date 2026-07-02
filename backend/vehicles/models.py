#Hier wird die Datenbankstruktur der Anwendung für die Datenbank deffiniert (RH, NW)


from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def validate_year(value):
    """
    Baujahr muss plausibel sein: nicht vor 1900 und nicht mehr als ein
    Jahr in der Zukunft (neue Modelljahre werden teils vorab gelistet).

    Als eigene Funktion (statt fixer MinValueValidator/MaxValueValidator-
    Grenzen), weil die Obergrenze vom aktuellen Jahr abhaengt und sich
    damit automatisch mitzieht statt in einer Migration einzufrieren.
    """
    aktuelles_jahr = date.today().year
    if value < 1900 or value > aktuelles_jahr + 1:
        raise ValidationError(
            f"Baujahr muss zwischen 1900 und {aktuelles_jahr + 1} liegen."
        )


class Vehicle(models.Model):

    # ── Basisdaten ────────────────────────────────────────────────────
    brand   = models.CharField(max_length=50, verbose_name="Marke")
    model   = models.CharField(max_length=100, verbose_name="Modell")
    year    = models.IntegerField(
        verbose_name="Baujahr",
        validators=[validate_year],
    )
    mileage = models.IntegerField(
        verbose_name="Kilometerstand",
        validators=[
            MinValueValidator(0, message="Kilometerstand darf nicht negativ sein."),
            MaxValueValidator(1_000_000, message="Kilometerstand wirkt unrealistisch (max. 1.000.000 km)."),
        ],
    )
    price   = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preis",
        validators=[
            MinValueValidator(Decimal("0.01"), message="Preis muss größer als 0 sein."),
        ],
    )

    STATUS = [
        ("available", "Verfügbar"),
        ("reserved",  "Reserviert"),
        ("sold",      "Verkauft"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="available",
        verbose_name="Status"
    )

    # ── Technische Details ────────────────────────────────────────────
    KRAFTSTOFF_CHOICES = [
        ("benzin",    "Benzin"),
        ("diesel",    "Diesel"),
        ("elektro",   "Elektro"),
        ("hybrid",    "Hybrid"),
        ("plug_in",   "Plug-in-Hybrid"),
        ("lpg",       "Autogas (LPG)"),
        ("erdgas",    "Erdgas (CNG)"),
        ("wasserstoff", "Wasserstoff"),
        ("sonstige",  "Sonstige"),
    ]
    kraftstoff = models.CharField(
        max_length=20,
        choices=KRAFTSTOFF_CHOICES,
        default="benzin",
        verbose_name="Kraftstoff"
    )

    GETRIEBE_CHOICES = [
        ("manuell",    "Schaltgetriebe"),
        ("automatik",  "Automatik"),
        ("halbautomatik", "Halbautomatik"),
    ]
    getriebe = models.CharField(
        max_length=20,
        choices=GETRIEBE_CHOICES,
        default="manuell",
        verbose_name="Getriebe"
    )

    leistung = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Leistung (PS)",
        validators=[
            MinValueValidator(1, message="Leistung muss größer als 0 sein."),
            MaxValueValidator(2000, message="Leistung wirkt unrealistisch (max. 2000 PS)."),
        ],
    )

    farbe = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="Farbe"
    )

    # ── Zulassung & Hauptuntersuchung ─────────────────────────────────
    # Format: "MM/YYYY" z.B. "03/2021"
    ez = models.CharField(
        max_length=7,
        blank=True,
        default="",
        verbose_name="Erstzulassung"
    )

    hu = models.CharField(
        max_length=7,
        blank=True,
        default="",
        verbose_name="HU bis"
    )

    tueren = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Türanzahl",
        validators=[
            MinValueValidator(1, message="Türanzahl muss mindestens 1 sein."),
            MaxValueValidator(8, message="Türanzahl wirkt unrealistisch (max. 8)."),
        ],
    )

    # ── Beschreibung & Ausstattung ────────────────────────────────────
    beschreibung = models.TextField(
        blank=True,
        default="",
        verbose_name="Beschreibung"
    )

    # Ausstattungsmerkmale als JSON-Liste, z.B. ["Navi", "Ledersitze"]
    ausstattung = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Ausstattung"
    )

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image_url = models.URLField(
        max_length=500,
        verbose_name="Bild-URL"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Bild für {self.vehicle}"


class PriceHistory(models.Model):
    """Speichert Preisänderungen eines Fahrzeugs über die Zeit."""

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="price_history"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preis",
        validators=[
            MinValueValidator(Decimal("0.01"), message="Preis muss größer als 0 sein."),
        ],
    )

    recorded_at = models.DateField(
        auto_now_add=True,
        verbose_name="Datum"
    )

    note = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Notiz"
    )

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.vehicle} – {self.price} € ({self.recorded_at})"