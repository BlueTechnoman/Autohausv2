#Hier wird die Pagination fuer die Fahrzeugliste konfiguriert (RH, NW)

from rest_framework.pagination import PageNumberPagination


class VehiclePagination(PageNumberPagination):
    """
    Pagination fuer GET /api/vehicles/.

    Standardmaessig 12 Fahrzeuge pro Seite (passt gut zu einem
    3- oder 4-spaltigen Grid im Frontend). Der Client kann die
    Seitengroesse ueber ?page_size=... selbst anpassen, aber nicht
    ueber 100 hinaus (verhindert versehentliche/absichtliche
    "gib mir alles auf einmal"-Anfragen, die den Server belasten).
    """

    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 100