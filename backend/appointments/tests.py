#Hier werden automatisierte Test angelegt mit denen man den Code Prüft
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from .models import Appointment

User = get_user_model()


class AppointmentVisibilityTests(APITestCase):
    """
    Tests dass Kunden nur ihre eigenen Termine sehen,
    Mitarbeiter/Admins aber alle Termine.
    """

    url = "/api/appointments/"

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

        self.appointment1 = Appointment.objects.create(
            customer=self.customer,
            appointment_type="test_drive",
            appointment_date=timezone.now(),
        )
        self.appointment2 = Appointment.objects.create(
            customer=self.other_customer,
            appointment_type="consultation",
            appointment_date=timezone.now(),
        )

    def test_anonymous_cannot_list_appointments(self):
        response = self.client.get(self.url)
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_customer_only_sees_own_appointments(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [a["id"] for a in response.data]
        self.assertEqual(ids, [self.appointment1.id])

    def test_employee_sees_all_appointments(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {a["id"] for a in response.data}
        self.assertEqual(ids, {self.appointment1.id, self.appointment2.id})


class AppointmentCreateTests(APITestCase):
    """Tests für POST /api/appointments/"""

    url = "/api/appointments/"

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="kunde3", password="testpasswort123", role="customer"
        )
        self.customer = Customer.objects.create(
            user=self.customer_user, first_name="Tom", last_name="Test",
            email="tom@example.com", phone="0123456780",
        )

    def test_create_requires_authentication(self):
        response = self.client.post(self.url, {
            "customer": self.customer.id,
            "appointment_type": "test_drive",
            "appointment_date": timezone.now().isoformat(),
        })

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertEqual(Appointment.objects.count(), 0)

    def test_create_with_authentication_succeeds(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "customer": self.customer.id,
            "appointment_type": "test_drive",
            "appointment_date": timezone.now().isoformat(),
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.first().status, "pending")

    def test_invalid_appointment_type_is_rejected(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "customer": self.customer.id,
            "appointment_type": "does_not_exist",
            "appointment_date": timezone.now().isoformat(),
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)