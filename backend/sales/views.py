#Hier wird die Logik der Anwendung festgelegt. Eine View verarbeitet eine Anfrage, 
#führt dann den benötigten Code aus und gibt eine Antwort (RH, NW)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()   # WICHTIG
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "customer":
            return Sale.objects.filter(
                customer__user=user
            ).select_related(
                "customer",
                "vehicle"
            )

        return Sale.objects.all().select_related(
            "customer",
            "vehicle"
        )