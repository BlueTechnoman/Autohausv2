#Hier wird das Python-Objekt in eine JSON umgewandelt und andersrum (RH, NW)
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
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

    def validate_password(self, value):
        """
        Prueft das Passwort gegen die in AUTH_PASSWORD_VALIDATORS
        konfigurierten Regeln (Mindestlaenge, nicht zu haeufig,
        nicht rein numerisch, nicht zu aehnlich zu Username/E-Mail).
        """
        # Temporaere, nicht gespeicherte User-Instanz - wird nur fuer den
        # UserAttributeSimilarityValidator gebraucht (Passwort darf nicht
        # zu aehnlich zu Username/E-Mail sein).
        temp_user = User(
            username=self.initial_data.get("username", ""),
            email=self.initial_data.get("email", ""),
        )

        try:
            validate_password(value, user=temp_user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))

        return value

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