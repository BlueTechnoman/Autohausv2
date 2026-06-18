from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

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