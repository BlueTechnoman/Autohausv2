#Hier wird die Datenbankstruktur der Anwendung für die Datenbank deffiniert (RH, NW)


from django.db import models


class Vehicle(models.Model):

    # ── Basisdaten ────────────────────────────────────────────────────
    brand   = models.CharField(max_length=50, verbose_name="Marke")
    model   = models.CharField(max_length=100, verbose_name="Modell")
    year    = models.IntegerField(verbose_name="Baujahr")
    mileage = models.IntegerField(verbose_name="Kilometerstand")
    price   = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis")

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
        verbose_name="Leistung (PS)"
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
        verbose_name="Türanzahl"
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
        verbose_name="Preis"
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