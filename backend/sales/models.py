from django.db import models

# Create your models here.

from django.db import models
from customers.models import Customer
from vehicles.models import Vehicle

class Sale(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="sales"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    STATUS = [
        ("offer", "Angebot"),
        ("sold", "Verkauft"),
    ]

    status = models.CharField(max_length=20, choices=STATUS, default="offer")

    def __str__(self):
        return f"{self.customer} - {self.vehicle}"