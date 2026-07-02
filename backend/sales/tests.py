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


class CheckoutTests(APITestCase):
    """Tests für POST /api/sales/checkout/ - der eigentliche Warenkorb-Checkout."""

    url = "/api/sales/checkout/"

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="checkoutkunde", password="testpasswort123", role="customer"
        )
        self.vehicle1 = make_vehicle(brand="BMW", model="320d")
        self.vehicle2 = make_vehicle(brand="Audi", model="A4")

    def test_checkout_requires_authentication(self):
        response = self.client.post(self.url, {"vehicle_ids": [self.vehicle1.id]})

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertEqual(Sale.objects.count(), 0)

    def test_checkout_with_empty_cart_is_rejected(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {"vehicle_ids": []})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sale.objects.count(), 0)

    def test_checkout_creates_one_sale_per_vehicle(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "vehicle_ids": [self.vehicle1.id, self.vehicle2.id],
            "phone": "0151234567",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sale.objects.count(), 2)
        self.assertIn("order_number", response.data)
        self.assertEqual(len(response.data["sales"]), 2)

        # Beide Sale-Zeilen teilen sich dieselbe order_number
        order_numbers = set(Sale.objects.values_list("order_number", flat=True))
        self.assertEqual(len(order_numbers), 1)

    def test_checkout_creates_customer_profile_if_missing(self):
        self.assertFalse(Customer.objects.filter(user=self.customer_user).exists())
        self.client.force_authenticate(user=self.customer_user)

        self.client.post(self.url, {
            "vehicle_ids": [self.vehicle1.id],
            "phone": "0151234567",
        })

        customer = Customer.objects.get(user=self.customer_user)
        self.assertEqual(customer.phone, "0151234567")

    def test_checkout_reserves_vehicles(self):
        self.client.force_authenticate(user=self.customer_user)

        self.client.post(self.url, {
            "vehicle_ids": [self.vehicle1.id],
            "phone": "0151234567",
        })

        self.vehicle1.refresh_from_db()
        self.assertEqual(self.vehicle1.status, "reserved")

    def test_checkout_rejects_already_reserved_vehicle(self):
        self.vehicle1.status = "reserved"
        self.vehicle1.save()
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "vehicle_ids": [self.vehicle1.id],
            "phone": "0151234567",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sale.objects.count(), 0)

    def test_checkout_is_all_or_nothing(self):
        """
        Warenkorb mit einem verfügbaren und einem bereits verkauften
        Fahrzeug: darf GAR NICHTS anlegen, nicht nur teilweise.
        """
        self.vehicle2.status = "sold"
        self.vehicle2.save()
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "vehicle_ids": [self.vehicle1.id, self.vehicle2.id],
            "phone": "0151234567",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sale.objects.count(), 0)
        self.vehicle1.refresh_from_db()
        self.assertEqual(self.vehicle1.status, "available")

    def test_checkout_with_unknown_vehicle_id_is_rejected(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "vehicle_ids": [999999],
            "phone": "0151234567",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sale.objects.count(), 0)

    def test_second_checkout_reuses_existing_customer_profile(self):
        self.client.force_authenticate(user=self.customer_user)

        # Erster Checkout legt das Customer-Profil an
        self.client.post(self.url, {"vehicle_ids": [self.vehicle1.id], "phone": "0151234567"})
        self.assertEqual(Customer.objects.filter(user=self.customer_user).count(), 1)

        # Zweiter Checkout darf KEIN zweites Profil anlegen
        self.client.post(self.url, {"vehicle_ids": [self.vehicle2.id]})
        self.assertEqual(Customer.objects.filter(user=self.customer_user).count(), 1)
        self.assertEqual(Sale.objects.filter(customer__user=self.customer_user).count(), 2)