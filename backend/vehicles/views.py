#Hier wird die Logik der Anwendung festgelegt. Eine View verarbeitet eine Anfrage, 
#führt dann den benötigten Code aus und gibt eine Antwort (RH, NW)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, BasePermission
from django.db.models import Q

from .models import Vehicle, VehicleImage
from .serializers import VehicleSerializer, VehicleImageSerializer
from .pagination import VehiclePagination


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated


class VehicleViewSet(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = VehiclePagination

    def get_queryset(self):
        # Feste Sortierung (neueste zuerst) - ohne order_by() waere die
        # Reihenfolge zwischen Seiten nicht garantiert stabil (SQLite kann
        # sonst je nach Anfrage unterschiedlich sortieren).
        queryset = Vehicle.objects.all().order_by("-id")

        brand = self.request.query_params.get("brand")
        model = self.request.query_params.get("model")
        status = self.request.query_params.get("status")
        year = self.request.query_params.get("year")
        search = self.request.query_params.get("search")

        if brand:
            queryset = queryset.filter(
            brand__icontains=brand
            )

        if model:
            queryset = queryset.filter(
                model__icontains=model
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if year:
            queryset = queryset.filter(
                year=year
            )

        if search:
            queryset = queryset.filter(
                Q(brand__icontains=search) |
                Q(model__icontains=search)
            )

        return queryset
    

class VehicleImageViewSet(ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]