#Hier wird die Datenbankstruktur der Anwendung für die Datenbank deffiniert (RH, NW)
from django.db import models
from customers.models import Customer
from django.conf import settings


class Appointment(models.Model):

    APPOINTMENT_TYPES = [
        ("test_drive", "Probefahrt"),
        ("consultation", "Beratung"),
        ("delivery", "Fahrzeugübergabe"),
        ("service", "Werkstatt"),
    ]

    STATUS_CHOICES = [
        ("pending", "Offen"),
        ("confirmed", "Bestätigt"),
        ("completed", "Abgeschlossen"),
        ("cancelled", "Storniert"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    appointment_type = models.CharField(
        max_length=20,
        choices=APPOINTMENT_TYPES
    )

    appointment_date = models.DateTimeField()

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.appointment_date}"