from rest_framework import serializers
from .models import Vehicle, VehicleImage, PriceHistory


class VehicleImageSerializer(serializers.ModelSerializer):

    class Meta:
        model  = VehicleImage
        fields = ["id", "vehicle", "image_url", "uploaded_at"]


class PriceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model  = PriceHistory
        fields = ["id", "price", "recorded_at", "note"]


class VehicleSerializer(serializers.ModelSerializer):

    images        = VehicleImageSerializer(many=True, read_only=True)
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model  = Vehicle
        fields = [
            "id", "brand", "model", "year", "mileage", "price", "status",
            "kraftstoff", "getriebe", "leistung", "farbe", "ez", "hu", "tueren",
            "beschreibung", "ausstattung",
            "images", "price_history",
        ]