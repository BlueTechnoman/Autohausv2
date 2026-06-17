from django.db import models

class Vehicle(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    STATUS = [
        ("available", "Verfügbar"),
        ("reserved", "Reserviert"),
        ("sold", "Verkauft"),
    ]

    status = models.CharField(max_length=20, choices=STATUS, default="available")

    def __str__(self):
        return f"{self.brand} {self.model}"