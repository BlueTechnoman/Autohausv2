#Hier werden automatisierte Test angelegt mit denen man den Code Prüft

from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from vehicles.models import Vehicle
from .models import Sale

User = get_user_model()


def make_vehicle(**overrides):
    defaults = dict(
        brand="BMW", model="320d", year=2021, mileage=45000,
        price=Decimal("28900.00"), status="available",
    )
    defaults.update(overrides)
    return Vehicle.objects.create(**defaults)


class SaleVisibilityTests(APITestCase):
    """
    Tests dass Kunden nur ihre eigenen Verkäufe sehen,
    Mitarbeiter/Admins aber alle.
    """

    url = "/api/sales/"

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="kunde1", password="testpasswort123", role="customer"
        )
        self.other_customer_user = User.objects.create_user(
            username="kunde2", password="testpasswort123", role="customer"
        )
        self.employee_user = User.objects.create_user(
            username="mitarbeiter", password="testpasswort123", role="employee"
        )

        self.customer = Customer.objects.create(
            user=self.customer_user, first_name="Max", last_name="Muster",
            email="max@example.com", phone="0123456789",
        )
        self.other_customer = Customer.objects.create(
            user=self.other_customer_user, first_name="Erika", last_name="Muster",
            email="erika@example.com", phone="0987654321",
        )

        self.vehicle1 = make_vehicle(brand="BMW")
        self.vehicle2 = make_vehicle(brand="Audi")

        self.sale1 = Sale.objects.create(
            customer=self.customer, vehicle=self.vehicle1,
            price=Decimal("28900.00"), status="offer",
        )
        self.sale2 = Sale.objects.create(
            customer=self.other_customer, vehicle=self.vehicle2,
            price=Decimal("31000.00"), status="offer",
        )

    def test_anonymous_cannot_list_sales(self):
        response = self.client.get(self.url)
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_customer_only_sees_own_sales(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [s["id"] for s in response.data]
        self.assertEqual(ids, [self.sale1.id])

    def test_employee_sees_all_sales(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {s["id"] for s in response.data}
        self.assertEqual(ids, {self.sale1.id, self.sale2.id})


class SaleCreateTests(APITestCase):
    """Tests für die Verkaufslogik (validate_vehicle, status='sold' setzt Fahrzeug auf 'sold')."""

    url = "/api/sales/"

    def setUp(self):
        self.employee_user = User.objects.create_user(
            username="mitarbeiter2", password="testpasswort123", role="employee"
        )
        self.customer = Customer.objects.create(
            first_name="Max", last_name="Muster",
            email="max2@example.com", phone="0123456789",
        )

    def test_cannot_sell_already_sold_vehicle(self):
        sold_vehicle = make_vehicle(status="sold")
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.post(self.url, {
            "customer": self.customer.id,
            "vehicle": sold_vehicle.id,
            "price": "28900.00",
            "status": "offer",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_marking_sale_as_sold_updates_vehicle_status(self):
        vehicle = make_vehicle(status="available")
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.post(self.url, {
            "customer": self.customer.id,
            "vehicle": vehicle.id,
            "price": "28900.00",
            "status": "sold",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.status, "sold")