#Hier werden automatisierte Test angelegt mit denen man den Code Prüft
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from vehicles.models import Vehicle
from .models import Appointment

User = get_user_model()


def make_vehicle(**overrides):
    defaults = dict(
        brand="BMW", model="320d", year=2021, mileage=45000,
        price=Decimal("28900.00"), status="available",
    )
    defaults.update(overrides)
    return Vehicle.objects.create(**defaults)


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

    def test_filter_by_type(self):
        Appointment.objects.create(
            customer=self.customer, appointment_type="inquiry",
        )
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(self.url, {"type": "inquiry"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["appointment_type"], "inquiry")

    def test_response_includes_display_fields(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(f"{self.url}{self.appointment1.id}/")

        self.assertEqual(response.data["customer_name"], "Max Muster")
        self.assertEqual(response.data["type_display"], "Probefahrt")
        self.assertEqual(response.data["status_display"], "Offen")
        self.assertIsNone(response.data["vehicle_info"])


class AppointmentCreateTests(APITestCase):
    """Tests für POST /api/appointments/ - customer wird automatisch gesetzt."""

    url = "/api/appointments/"

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="kunde3", password="testpasswort123", role="customer"
        )

    def test_create_requires_authentication(self):
        response = self.client.post(self.url, {
            "appointment_type": "test_drive",
            "appointment_date": timezone.now().isoformat(),
        })

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertEqual(Appointment.objects.count(), 0)

    def test_create_auto_creates_customer_profile(self):
        self.assertFalse(Customer.objects.filter(user=self.customer_user).exists())
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "appointment_type": "test_drive",
            "appointment_date": timezone.now().isoformat(),
            "message": "Ich haette gerne eine Probefahrt.",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.customer.user, self.customer_user)
        self.assertEqual(appointment.status, "pending")
        self.assertEqual(appointment.message, "Ich haette gerne eine Probefahrt.")

    def test_create_without_date_succeeds(self):
        # z.B. bei einer allgemeinen Anfrage (type="inquiry") ist oft noch
        # kein festes Datum bekannt.
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "appointment_type": "inquiry",
            "message": "Ist das Fahrzeug noch verfuegbar?",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(Appointment.objects.first().appointment_date)

    def test_create_with_vehicle_reference(self):
        vehicle = make_vehicle()
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "appointment_type": "inquiry",
            "vehicle": vehicle.id,
            "message": "Interessiert an diesem Fahrzeug.",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["vehicle_info"], "BMW 320d (2021)")

    def test_customer_cannot_set_someone_elses_customer_id(self):
        """
        Regressionstest: 'customer' im Body darf ignoriert werden -
        ein Kunde darf sich nicht als jemand anderes ausgeben.
        """
        other_user = User.objects.create_user(
            username="anderer", password="testpasswort123", role="customer"
        )
        other_customer = Customer.objects.create(
            user=other_user, first_name="Anderer", last_name="User",
            email="anderer@example.com", phone="0000000000",
        )
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "customer": other_customer.id,
            "appointment_type": "inquiry",
            "message": "Test",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Appointment.objects.get(id=response.data["id"])
        self.assertNotEqual(created.customer, other_customer)
        self.assertEqual(created.customer.user, self.customer_user)

    def test_invalid_appointment_type_is_rejected(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "appointment_type": "does_not_exist",
            "appointment_date": timezone.now().isoformat(),
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AppointmentReplyTests(APITestCase):
    """Tests für PATCH /api/appointments/{id}/reply/"""

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="kunde4", password="testpasswort123", role="customer"
        )
        self.employee_user = User.objects.create_user(
            username="mitarbeiter2", password="testpasswort123", role="employee"
        )
        self.customer = Customer.objects.create(
            user=self.customer_user, first_name="Tom", last_name="Test",
            email="tom@example.com", phone="0123456780",
        )
        self.appointment = Appointment.objects.create(
            customer=self.customer, appointment_type="inquiry",
            message="Ist das Fahrzeug noch da?",
        )
        self.url = f"/api/appointments/{self.appointment.id}/reply/"

    def test_customer_cannot_reply(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.patch(self.url, {
            "admin_reply": "Ja, noch verfuegbar!",
            "status": "confirmed",
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.admin_reply, "")

    def test_employee_can_reply(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.patch(self.url, {
            "admin_reply": "Ja, noch verfuegbar!",
            "status": "confirmed",
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.admin_reply, "Ja, noch verfuegbar!")
        self.assertEqual(self.appointment.status, "confirmed")
        self.assertEqual(self.appointment.employee, self.employee_user)

    def test_customer_cannot_set_admin_reply_via_normal_update(self):
        """
        Regressionstest: admin_reply/status duerfen nicht am reply()-Endpoint
        vorbei ueber ein normales PATCH auf /api/appointments/{id}/ gesetzt
        werden koennen.
        """
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.patch(f"/api/appointments/{self.appointment.id}/", {
            "admin_reply": "Ich antworte mir selbst!",
        })

        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.admin_reply, "")