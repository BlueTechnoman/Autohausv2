#Hier wird die Logik der Anwendung festgelegt. Eine View verarbeitet eine Anfrage, 
#führt dann den benötigten Code aus und gibt eine Antwort (RH, NW)

import uuid

from django.db import transaction
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from customers.models import Customer
from vehicles.models import Vehicle
from .models import Sale
from .serializers import SaleSerializer, CheckoutSerializer


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

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        """
        POST /api/sales/checkout/
        Body: { "vehicle_ids": [1, 2, 3], "phone": "0151..." (optional) }

        Erstellt aus dem Warenkorb (Liste von Fahrzeug-IDs) fuer den
        eingeloggten User pro Fahrzeug eine Sale-Zeile (status="offer",
        also ein Angebot/eine Reservierungsanfrage, keine final bestaetigte
        Verkaufsabwicklung - das bleibt Mitarbeitern im Backoffice
        vorbehalten). Alle Zeilen eines Checkouts teilen sich dieselbe
        order_number.

        Alles passiert in einer Transaktion: entweder werden ALLE
        Fahrzeuge erfolgreich reserviert, oder (z.B. weil eines davon
        zwischenzeitlich schon verkauft wurde) gar keins - kein
        halbfertiger Warenkorb.
        """
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle_ids = serializer.validated_data["vehicle_ids"]
        phone = serializer.validated_data.get("phone", "")

        with transaction.atomic():
            # Customer-Profil des eingeloggten Users holen oder anlegen.
            # Customer.phone ist ein Pflichtfeld - falls beim allerersten
            # Checkout noch keins hinterlegt ist, wird die mitgeschickte
            # Telefonnummer verwendet.
            customer, created = Customer.objects.get_or_create(
                user=request.user,
                defaults={
                    "first_name": request.user.username,
                    "last_name": "",
                    "email": request.user.email or f"{request.user.username}@platzhalter.invalid",
                    "phone": phone,
                },
            )
            if not created and phone and not customer.phone:
                customer.phone = phone
                customer.save(update_fields=["phone"])

            vehicles = list(Vehicle.objects.filter(id__in=vehicle_ids))
            found_ids = {v.id for v in vehicles}
            missing_ids = set(vehicle_ids) - found_ids
            if missing_ids:
                raise ValidationError({
                    "vehicle_ids": f"Fahrzeuge nicht gefunden: {sorted(missing_ids)}"
                })

            nicht_verfuegbar = [v for v in vehicles if v.status != "available"]
            if nicht_verfuegbar:
                raise ValidationError({
                    "vehicle_ids": [
                        f"{v.brand} {v.model} ist nicht mehr verfügbar (Status: {v.get_status_display()})."
                        for v in nicht_verfuegbar
                    ]
                })

            order_number = f"AH-{uuid.uuid4().hex[:8].upper()}"
            sales = []
            for vehicle in vehicles:
                sale = Sale.objects.create(
                    customer=customer,
                    vehicle=vehicle,
                    price=vehicle.price,
                    status="offer",
                    order_number=order_number,
                )
                vehicle.status = "reserved"
                vehicle.save(update_fields=["status"])
                sales.append(sale)

        return Response(
            {
                "order_number": order_number,
                "sales": SaleSerializer(sales, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )