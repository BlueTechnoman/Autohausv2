#Hier wird die Logik der Anwendung festgelegt. Eine View verarbeitet eine Anfrage, 
#führt dann den benötigten Code aus und gibt eine Antwort (RH, NW)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "customer":
            return Customer.objects.filter(user=user)

        return Customer.objects.all()