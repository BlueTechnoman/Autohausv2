from rest_framework import serializers
from .models import Vehicle, VehicleImage, PriceHistory


class VehicleImageSerializer(serializers.ModelSerializer):

    # Absolute URL des Bildes – direkt im Serializer gebaut,
    # damit das Frontend nicht selbst /media/ voranstellen muss.
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = VehicleImage
        fields = ["id", "vehicle", "image", "image_url", "uploaded_at"]

    def get_image_url(self, obj) -> str | None:
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


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
            "id",
            "brand",
            "model",
            "year",
            "mileage",
            "price",
            "status",
            # Technische Details
            "kraftstoff",
            "getriebe",
            "leistung",
            "farbe",
            "ez",
            "hu",
            "tueren",
            # Beschreibung & Ausstattung
            "beschreibung",
            "ausstattung",
            # Relationen
            "images",
            "price_history",
        ]