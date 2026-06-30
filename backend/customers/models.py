#Hier wird die Datenbankstruktur der Anwendung für die Datenbank deffiniert (RH, NW)

from django.db import models
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"