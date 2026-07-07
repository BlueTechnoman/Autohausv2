#Hier werden automatisierte Test angelegt mit denen man den Code Prüft


from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from vehicles.models import Vehicle

User = get_user_model()


class DashboardTests(APITestCase):
    """Tests für GET /api/dashboard/"""

    url = "/api/dashboard/"

    def setUp(self):
        self.user = User.objects.create_user(
            username="mitarbeiter", password="testpasswort123", role="employee"
        )

        Customer.objects.create(
            first_name="Max", last_name="Muster",
            email="max@example.com", phone="0123456789",
        )
        Vehicle.objects.create(
            brand="BMW", model="320d", year=2021, mileage=45000,
            price=Decimal("28900.00"), status="available",
        )
        Vehicle.objects.create(
            brand="Audi", model="A4", year=2020, mileage=60000,
            price=Decimal("22900.00"), status="available",
        )

    def test_dashboard_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_dashboard_returns_correct_counts(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["customers"], 1)
        self.assertEqual(response.data["vehicles"], 2)
        self.assertEqual(response.data["sales"], 0)
        self.assertEqual(response.data["appointments"], 0)
        self.assertEqual(response.data["documents"], 0)