#Hier wird das Python-Objekt in eine JSON umgewandelt und andersrum (RH, NW)

from rest_framework import serializers
from .models import Sale
from customers.serializers import CustomerSerializer
from vehicles.serializers import VehicleSerializer


class SaleSerializer(serializers.ModelSerializer):
    customer_detail = CustomerSerializer(
        source="customer",
        read_only=True
    )

    vehicle_detail = VehicleSerializer(
        source="vehicle",
        read_only=True
    )

    class Meta:
        model = Sale
        fields = [
            "id",
            "customer",
            "vehicle",
            "price",
            "date",
            "status",
            "customer_detail",
            "vehicle_detail",
        ]

    def validate_vehicle(self, vehicle):
        if vehicle.status == "sold":
            raise serializers.ValidationError(
                "Fahrzeug wurde bereits verkauft."
            )

        return vehicle