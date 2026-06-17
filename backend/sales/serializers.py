from rest_framework import serializers
from .models import Sale
from customers.serializers import CustomerSerializer
from vehicles.serializers import VehicleSerializer

class SaleSerializer(serializers.ModelSerializer):
    customer_detail = CustomerSerializer(source="customer", read_only=True)
    vehicle_detail = VehicleSerializer(source="vehicle", read_only=True)

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