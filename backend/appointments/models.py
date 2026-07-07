#Hier wird die Datenbankstruktur der Anwendung für die Datenbank deffiniert (RH, NW)
from django.db import models
from customers.models import Customer
from vehicles.models import Vehicle
from django.conf import settings


class Appointment(models.Model):

    APPOINTMENT_TYPES = [
        ("test_drive",   "Probefahrt"),
        ("consultation", "Beratung"),
        ("delivery",     "Fahrzeugübergabe"),
        ("service",      "Werkstatt"),
        # Allgemeine Fahrzeuganfrage ohne festen Termin - wird im Frontend
        # separat unter "Anfragen" (statt "Termine") verwaltet.
        ("inquiry",      "Anfrage"),
    ]

    STATUS_CHOICES = [
        ("pending",   "Offen"),
        ("confirmed", "Bestätigt"),
        ("rejected",  "Abgelehnt"),
        ("completed", "Abgeschlossen"),
        ("cancelled", "Storniert"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    # Optional: Anfrage/Termin kann sich auf ein konkretes Fahrzeug beziehen
    # (z.B. "Probefahrt fuer diesen BMW"). Bei allgemeinen Anfragen leer.
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
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

    # Optional: bei reinen Anfragen (type="inquiry") ist oft noch kein
    # festes Datum bekannt.
    appointment_date = models.DateTimeField(null=True, blank=True)

    message = models.TextField(blank=True, default="")

    # Antwort eines Mitarbeiters/Admins auf die Anfrage. Wird NICHT vom
    # Kunden selbst gesetzt, sondern nur ueber die reply()-Action.
    admin_reply = models.TextField(blank=True, default="")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.appointment_date or 'ohne Datum'}"