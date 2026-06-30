#Hier wird die Datenbankstruktur der Anwendung für die Datenbank deffiniert (RH, NW)
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("employee", "Mitarbeiter"),
        ("customer", "Kunde"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )