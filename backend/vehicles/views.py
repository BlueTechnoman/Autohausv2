import urllib.request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.db.models import Q

from .models import Vehicle, VehicleImage
from .serializers import VehicleSerializer, VehicleImageSerializer


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class VehicleViewSet(ModelViewSet):
    serializer_class   = VehicleSerializer
    queryset           = Vehicle.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        brand  = self.request.query_params.get("brand")
        model  = self.request.query_params.get("model")
        status = self.request.query_params.get("status")
        year   = self.request.query_params.get("year")
        search = self.request.query_params.get("search")

        if brand:  queryset = queryset.filter(brand__icontains=brand)
        if model:  queryset = queryset.filter(model__icontains=model)
        if status: queryset = queryset.filter(status=status)
        if year:   queryset = queryset.filter(year=year)
        if search:
            queryset = queryset.filter(
                Q(brand__icontains=search) | Q(model__icontains=search)
            )
        return queryset


class VehicleImageViewSet(ModelViewSet):
    queryset           = VehicleImage.objects.all()
    serializer_class   = VehicleImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(["GET"])
@permission_classes([AllowAny])
def proxy_image(request):
    """
    Lädt ein externes Bild (z.B. von Wikimedia) serverseitig und
    leitet es an den Browser weiter – umgeht den 403-Hotlink-Schutz.

    Aufruf: GET /api/proxy-image/?url=https://upload.wikimedia.org/...
    """
    url = request.query_params.get("url", "")

    # Nur Wikimedia-URLs erlauben
    if not url.startswith("https://upload.wikimedia.org/"):
        return HttpResponse("Ungültige URL", status=400)

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "AutohausApp/1.0 (https://github.com/dein-repo; dein@email.de)",
                "Referer":    "https://commons.wikimedia.org/",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            content_type = resp.headers.get("Content-Type", "image/jpeg")
            data = resp.read()
        return HttpResponse(data, content_type=content_type)

    except Exception as e:
        return HttpResponse(f"Fehler: {e}", status=502)