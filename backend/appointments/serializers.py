#Hier wird das Python-Objekt in eine JSON umgewandelt und andersrum (RH, NW)
from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"