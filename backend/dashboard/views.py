from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from customers.models import Customer
from vehicles.models import Vehicle
from sales.models import Sale
from appointments.models import Appointment
from documents.models import Document


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "customers": Customer.objects.count(),
            "vehicles": Vehicle.objects.count(),
            "sales": Sale.objects.count(),
            "appointments": Appointment.objects.count(),
            "documents": Document.objects.count(),
        })