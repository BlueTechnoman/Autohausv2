# Tests fuer die zentrale Fehlerbehandlung (Autohaus/exceptions.py)

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework import status
from rest_framework.test import APITestCase

from .exceptions import custom_exception_handler

User = get_user_model()


class ExceptionHandlerUnitTests(APITestCase):
    """
    Ruft custom_exception_handler() direkt auf (ohne HTTP-Request),
    um alle Zweige der Fehlerbehandlung isoliert zu testen -
    inklusive Faellen wie Http404 und unerwartete Server-Bugs,
    die schwer ueber echte Endpunkte zu provozieren sind.
    """

    def test_validation_error_has_unified_envelope(self):
        exc = drf_exceptions.ValidationError({"username": ["Dieses Feld ist erforderlich."]})

        response = custom_exception_handler(exc, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["error"])
        self.assertEqual(response.data["status_code"], status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data["message"])
        self.assertEqual(
            response.data["details"], {"username": ["Dieses Feld ist erforderlich."]}
        )

    def test_not_authenticated_has_unified_envelope(self):
        exc = drf_exceptions.NotAuthenticated()

        response = custom_exception_handler(exc, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data["error"])
        self.assertIsInstance(response.data["message"], str)

    def test_permission_denied_has_unified_envelope(self):
        exc = drf_exceptions.PermissionDenied()

        response = custom_exception_handler(exc, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(response.data["error"])

    def test_django_http404_is_handled(self):
        exc = Http404("Fahrzeug nicht gefunden")

        response = custom_exception_handler(exc, {})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.data["error"])
        self.assertIn("nicht gefunden", response.data["message"])

    def test_django_permission_denied_is_handled(self):
        exc = DjangoPermissionDenied("nope")

        response = custom_exception_handler(exc, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(response.data["error"])

    def test_unexpected_exception_returns_generic_500_without_leaking_details(self):
        """
        Ein ganz unerwarteter Bug (z.B. KeyError irgendwo im View-Code)
        darf dem Client NIEMALS den echten Fehlertext/Stacktrace zeigen -
        nur eine generische Meldung mit Status 500.
        """
        exc = KeyError("geheimer_interner_feldname")

        response = custom_exception_handler(exc, {})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue(response.data["error"])
        self.assertNotIn("geheimer_interner_feldname", str(response.data["message"]))
        self.assertIsNone(response.data["details"])


class ExceptionHandlerIntegrationTests(APITestCase):
    """
    Testet das einheitliche Fehlerformat ueber echte HTTP-Endpunkte,
    damit sichergestellt ist dass der Handler auch wirklich in
    REST_FRAMEWORK.EXCEPTION_HANDLER eingehaengt ist.
    """

    def test_404_on_unknown_vehicle_has_unified_envelope(self):
        response = self.client.get("/api/vehicles/999999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.data["error"])
        self.assertEqual(response.data["status_code"], status.HTTP_404_NOT_FOUND)

    def test_401_on_protected_endpoint_has_unified_envelope(self):
        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data["error"])
        self.assertIn("message", response.data)

    def test_400_on_invalid_register_has_unified_envelope_with_field_details(self):
        response = self.client.post("/api/accounts/register/", {
            "username": "",
            "password": "x",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data["error"])
        self.assertIsInstance(response.data["details"], dict)
        self.assertTrue(
            "username" in response.data["details"] or "password" in response.data["details"]
        )