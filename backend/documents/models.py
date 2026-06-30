#Hier wird die Datenbankstruktur der Anwendung für die Datenbank deffiniert (RH, NW)

from django.db import models
from customers.models import Customer


class Document(models.Model):

    DOCUMENT_TYPES = [
        ("contract", "Kaufvertrag"),
        ("invoice", "Rechnung"),
        ("id_card", "Ausweis"),
        ("vehicle_doc", "Fahrzeugdokument"),
        ("other", "Sonstiges"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(max_length=255)

    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
        default="other"
    )

    file = models.FileField(
        upload_to="documents/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title