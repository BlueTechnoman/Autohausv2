from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, BasePermission
from django.db.models import Q

from .models import Vehicle, VehicleImage
from .serializers import VehicleSerializer, VehicleImageSerializer


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated


class VehicleViewSet(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Vehicle.objects.all()

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
