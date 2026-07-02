#Hier wird die Logik der Anwendung festgelegt. Eine View verarbeitet eine Anfrage, 
#führt dann den benötigten Code aus und gibt eine Antwort (RH, NW)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response

from customers.models import Customer
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentReplySerializer


class IsEmployeeOrAdmin(BasePermission):
    """Nur Mitarbeiter/Admins duerfen auf Anfragen antworten."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("employee", "admin")
        )


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "customer":
            queryset = Appointment.objects.filter(customer__user=user)
        else:
            queryset = Appointment.objects.all()

        # Optionaler Filter, z.B. ?type=inquiry (Anfragen-Uebersicht im
        # Admin-Bereich zeigt nur Fahrzeuganfragen, keine Kalendertermine)
        appointment_type = self.request.query_params.get("type")
        if appointment_type:
            queryset = queryset.filter(appointment_type=appointment_type)

        return queryset.select_related("customer", "vehicle", "employee")

    def perform_create(self, serializer):
        # "customer" kommt NIE aus dem Request-Body (read_only im
        # Serializer) - stattdessen wird das Customer-Profil des
        # eingeloggten Users automatisch geholt oder angelegt (analog zum
        # Checkout-Flow in sales/views.py).
        customer, _ = Customer.objects.get_or_create(
            user=self.request.user,
            defaults={
                "first_name": self.request.user.username,
                "last_name": "",
                "email": self.request.user.email or f"{self.request.user.username}@platzhalter.invalid",
                "phone": "",
            },
        )
        serializer.save(customer=customer)

    @action(detail=True, methods=["patch"], permission_classes=[IsEmployeeOrAdmin])
    def reply(self, request, pk=None):
        """
        PATCH /api/appointments/{id}/reply/
        Body: { "admin_reply": "...", "status": "confirmed" }

        Nur fuer Mitarbeiter/Admins - der Kunde selbst darf admin_reply
        und status nicht ueber das normale PATCH/PUT setzen (siehe
        read_only_fields im AppointmentSerializer).
        """
        appointment = self.get_object()
        serializer = AppointmentReplySerializer(
            appointment, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(employee=request.user)

        return Response(AppointmentSerializer(appointment).data)