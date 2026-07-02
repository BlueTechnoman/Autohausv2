#Hier werden automatisierte Test angelegt mit denen man den Code Prüft


from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Customer

User = get_user_model()


class CustomerVisibilityTests(APITestCase):
    """
    Tests dass Kunden nur ihren eigenen Datensatz sehen,
    Mitarbeiter/Admins aber alle Kunden.
    """

    url = "/api/customers/"

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

    def test_anonymous_cannot_list_customers(self):
        response = self.client.get(self.url)
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_customer_only_sees_own_record(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [c["id"] for c in response.data]
        self.assertEqual(ids, [self.customer.id])

    def test_employee_sees_all_customers(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {c["id"] for c in response.data}
        self.assertEqual(ids, {self.customer.id, self.other_customer.id})


class CustomerCreateTests(APITestCase):
    """Tests für POST /api/customers/"""

    url = "/api/customers/"

    def setUp(self):
        self.employee_user = User.objects.create_user(
            username="mitarbeiter2", password="testpasswort123", role="employee"
        )
        self.payload = {
            "first_name": "Anna",
            "last_name": "Beispiel",
            "email": "anna@example.com",
            "phone": "0151234567",
        }

    def test_create_requires_authentication(self):
        response = self.client.post(self.url, self.payload)

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_with_authentication_succeeds(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)

    def test_email_must_be_unique(self):
        Customer.objects.create(
            first_name="Anna", last_name="Beispiel",
            email="anna@example.com", phone="0151234567",
        )
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)