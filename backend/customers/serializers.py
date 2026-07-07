#Hier wird das Python-Objekt in eine JSON umgewandelt und andersrum (RH, NW)

from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"