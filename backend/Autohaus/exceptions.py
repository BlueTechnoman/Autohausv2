# Zentrale Fehlerbehandlung fuer die REST-API.
#
# Ohne das hier sieht jede Fehlerantwort anders aus (mal {"detail": "..."},
# mal {"feld": ["Fehler"]}, mal ein rohes Django-Http404 mit HTML-Seite).
# Dieser Handler sorgt dafuer, dass IMMER dasselbe JSON-Format zurueckkommt:
#
#   {
#       "error": true,
#       "status_code": 400,
#       "message": "Kurze, verstaendliche Meldung",
#       "details": {...}   # die urspruenglichen Fehlerdaten, z.B. pro Feld
#   }
#
# Wird in settings.py unter REST_FRAMEWORK -> EXCEPTION_HANDLER eingetragen.

import logging

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status as drf_status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_default_exception_handler

logger = logging.getLogger("django")


def _extract_message(data):
    """Baut aus den DRF-Fehlerdaten eine einzelne, lesbare Meldung."""

    if isinstance(data, dict):
        # Einfacher Fall: {"detail": "..."} (z.B. NotAuthenticated, NotFound)
        if "detail" in data and len(data) == 1:
            return str(data["detail"])

        # Validierungsfehler pro Feld: {"password": ["zu kurz"], ...}
        # -> erste Meldung des ersten Feldes nehmen
        for field, value in data.items():
            if isinstance(value, (list, tuple)) and value:
                return f"{field}: {value[0]}"
            if isinstance(value, str):
                return f"{field}: {value}"

        return "Ein Fehler ist aufgetreten."

    if isinstance(data, (list, tuple)) and data:
        return str(data[0])

    return "Ein Fehler ist aufgetreten."


def _error_response(message, status_code, details=None):
    return Response(
        {
            "error": True,
            "status_code": status_code,
            "message": message,
            "details": details,
        },
        status=status_code,
    )


def custom_exception_handler(exc, context):
    """
    Ersetzt rest_framework.views.exception_handler als globalen Handler.

    Ablauf:
    1. Der DRF-Standardhandler wird zuerst gefragt. Der kennt sich mit allen
       APIException-Unterklassen aus (ValidationError, NotAuthenticated,
       PermissionDenied, NotFound, Throttled, ...) und liefert dafuer eine
       passende Response.
    2. Falls der Standardhandler nichts damit anfangen kann (z.B. ein Http404
       aus einer get_object_or_404()-Abfrage, ein Django-PermissionDenied,
       oder ein ganz unerwarteter Bug wie ein KeyError/ZeroDivisionError),
       kuemmern wir uns selbst darum, statt eine haessliche 500-HTML-Seite
       oder einen rohen Stacktrace an den Client zu schicken.
    3. Unerwartete Fehler werden serverseitig geloggt, aber dem Client wird
       NUR eine generische Meldung gezeigt (kein Stacktrace, keine internen
       Details -> Sicherheit).
    """

    response = drf_default_exception_handler(exc, context)

    if response is not None:
        # DRF hat den Fehler bereits sauber behandelt - nur noch das
        # Antwortformat vereinheitlichen.
        response.data = {
            "error": True,
            "status_code": response.status_code,
            "message": _extract_message(response.data),
            "details": response.data,
        }
        return response

    if isinstance(exc, Http404):
        return _error_response(
            "Die angeforderte Ressource wurde nicht gefunden.",
            drf_status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, DjangoPermissionDenied):
        return _error_response(
            "Keine Berechtigung fuer diese Aktion.",
            drf_status.HTTP_403_FORBIDDEN,
        )

    # Alles andere ist ein unerwarteter Serverfehler (Bug, DB-Fehler, ...).
    # Serverseitig mit vollem Stacktrace loggen, dem Client aber nur eine
    # generische, ungefaehrliche Meldung schicken.
    logger.exception("Unerwarteter Serverfehler", exc_info=exc)

    return _error_response(
        "Es ist ein unerwarteter Fehler aufgetreten. Bitte versuche es spaeter erneut.",
        drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
    )