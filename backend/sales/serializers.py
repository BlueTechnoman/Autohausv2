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
            "order_number",
            "customer_detail",
            "vehicle_detail",
        ]
        read_only_fields = ["order_number"]

    def validate_vehicle(self, vehicle):
        if vehicle.status == "sold":
            raise serializers.ValidationError(
                "Fahrzeug wurde bereits verkauft."
            )

        return vehicle


class CheckoutSerializer(serializers.Serializer):
    """
    Eingabe-Serializer fuer POST /api/sales/checkout/.

    Nimmt die Fahrzeug-IDs aus dem Warenkorb entgegen und optional eine
    Telefonnummer, falls fuer den eingeloggten User noch kein Customer-
    Profil existiert (Customer.phone ist ein Pflichtfeld).
    """

    vehicle_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        min_length=1,
        error_messages={
            "empty": "Der Warenkorb ist leer.",
            "min_length": "Der Warenkorb ist leer.",
        },
    )
    phone = serializers.CharField(required=False, allow_blank=True, default="") 