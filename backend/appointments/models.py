from django.db import models

# Create your models here.

from customers.models import Customer

class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    date = models.DateTimeField()

    TYPE = [
        ("testdrive", "Probefahrt"),
        ("consulting", "Beratung"),
        ("handover", "Übergabe"),
    ]

    type = models.CharField(max_length=20, choices=TYPE)