from rest_framework import serializers
from .models import Vehicle, VehicleImage


class VehicleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleImage
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):

    images = VehicleImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "brand",
            "model",
            "year",
            "mileage",
            "price",
            "status",
            "images",
        ]