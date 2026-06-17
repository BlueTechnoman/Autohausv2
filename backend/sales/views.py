from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from .models import Sale
from .serializers import SaleSerializer

class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all().select_related("customer", "vehicle")
    serializer_class = SaleSerializer