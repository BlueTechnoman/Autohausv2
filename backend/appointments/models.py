from django.db import models

# Create your models here.

from django.db import models
from customers.models import Customer
from accounts.models import User

class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100)
    date = models.DateTimeField()

    TYPE_CHOICES = [
        ("testdrive", "Probefahrt"),
        ("consulting", "Beratung"),
        ("handover", "Übergabe"),
        ("service", "Werkstatt"),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)