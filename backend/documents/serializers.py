#Hier wird das Python-Objekt in eine JSON umgewandelt und andersrum (RH, NW)

from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"