#Hier wird das Python-Objekt in eine JSON umgewandelt und andersrum (RH, NW)
from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    # Anzeige-Felder fuers Frontend - nicht direkt im Model, sondern aus
    # den verknuepften Objekten (Customer, Vehicle) bzw. den choices
    # berechnet. Read-only, weil sie nur zur Darstellung dienen.
    customer_name = serializers.SerializerMethodField()
    vehicle_info = serializers.SerializerMethodField()
    type_display = serializers.CharField(source="get_appointment_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "customer",
            "customer_name",
            "vehicle",
            "vehicle_info",
            "employee",
            "appointment_type",
            "type_display",
            "appointment_date",
            "message",
            "admin_reply",
            "status",
            "status_display",
            "created_at",
        ]
        # "customer" wird serverseitig aus dem eingeloggten User bestimmt
        # (siehe AppointmentViewSet.perform_create) - ein Kunde darf sich
        # nicht als jemand anderes ausgeben.
        # "admin_reply" darf ein Kunde nicht selbst setzen - das passiert
        # ausschliesslich ueber die reply()-Action (nur fuer Mitarbeiter/Admin).
        read_only_fields = ["customer", "admin_reply"]

    def get_customer_name(self, obj):
        name = f"{obj.customer.first_name} {obj.customer.last_name}".strip()
        return name or obj.customer.email

    def get_vehicle_info(self, obj):
        if not obj.vehicle:
            return None
        return f"{obj.vehicle.brand} {obj.vehicle.model} ({obj.vehicle.year})"


class AppointmentReplySerializer(serializers.ModelSerializer):
    """
    Eingabe-Serializer fuer PATCH /api/appointments/{id}/reply/.
    Nur die Felder, die ein Mitarbeiter/Admin beim Beantworten setzen darf.
    """

    class Meta:
        model = Appointment
        fields = ["admin_reply", "status"]