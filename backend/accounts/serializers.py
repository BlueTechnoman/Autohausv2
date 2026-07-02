#Hier wird das Python-Objekt in eine JSON umgewandelt und andersrum (RH, NW)
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "role",
        ]
        # "role" darf beim Self-Service-Register nur gelesen, nicht gesetzt
        # werden - sonst koennte sich jeder z.B. role="admin" selbst geben.
        read_only_fields = ["role"]

    def create(self, validated_data):
        # Sicherheitsnetz: falls "role" trotz read_only_fields irgendwie
        # im validated_data landet, hier zusaetzlich hart ueberschreiben.
        validated_data.pop("role", None)

        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            role="customer",
        )