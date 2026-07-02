#Hier werden automatisierte Test angelegt mit denen man den Code Prüft


from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Vehicle

User = get_user_model()


def make_vehicle(**overrides):
    defaults = dict(
        brand="BMW",
        model="320d",
        year=2021,
        mileage=45000,
        price=Decimal("28900.00"),
        status="available",
    )
    defaults.update(overrides)
    return Vehicle.objects.create(**defaults)


class VehicleListTests(APITestCase):
    """
    Tests für GET /api/vehicles/ - öffentlich, kein Login nötig.

    Die Liste ist paginiert, die Antwort hat also die Form
    {"count": ..., "next": ..., "previous": ..., "results": [...]}
    statt einer nackten Liste.
    """

    url = "/api/vehicles/"

    def test_list_is_public(self):
        make_vehicle()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_returns_expected_fields(self):
        make_vehicle(brand="Audi", model="A4")
        response = self.client.get(self.url)

        item = response.data["results"][0]
        self.assertEqual(item["brand"], "Audi")
        self.assertEqual(item["model"], "A4")
        self.assertIn("images", item)
        self.assertIn("price_history", item)

    def test_detail_returns_single_vehicle(self):
        vehicle = make_vehicle()
        response = self.client.get(f"{self.url}{vehicle.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], vehicle.id)

    def test_detail_unknown_id_returns_404(self):
        response = self.client.get(f"{self.url}999999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VehiclePaginationTests(APITestCase):
    """Tests speziell für das Pagination-Verhalten (?page=, ?page_size=)."""

    url = "/api/vehicles/"

    def setUp(self):
        # 15 Fahrzeuge anlegen - mehr als die Standard-Seitengroesse (12)
        for i in range(15):
            make_vehicle(model=f"Modell-{i}")

    def test_default_page_size_is_12(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 12)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    def test_second_page_contains_remaining_items(self):
        response = self.client.get(self.url, {"page": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertIsNone(response.data["next"])
        self.assertIsNotNone(response.data["previous"])

    def test_custom_page_size(self):
        response = self.client.get(self.url, {"page_size": 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

    def test_page_size_is_capped_at_max(self):
        response = self.client.get(self.url, {"page_size": 1000})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # max_page_size=100, aber es gibt nur 15 Fahrzeuge -> alle 15 kommen
        self.assertEqual(len(response.data["results"]), 15)

    def test_unknown_page_returns_404(self):
        response = self.client.get(self.url, {"page": 999})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VehicleFilterTests(APITestCase):
    """Tests für die Query-Parameter (?brand=, ?status=, ?search=, ...)"""

    url = "/api/vehicles/"

    def setUp(self):
        make_vehicle(brand="BMW", model="320d", status="available")
        make_vehicle(brand="Audi", model="A4", status="reserved")
        make_vehicle(brand="BMW", model="M3", status="sold")

    def test_filter_by_brand(self):
        response = self.client.get(self.url, {"brand": "BMW"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertTrue(all(v["brand"] == "BMW" for v in response.data["results"]))

    def test_filter_by_status(self):
        response = self.client.get(self.url, {"status": "reserved"})

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["model"], "A4")

    def test_search_matches_brand_or_model(self):
        response = self.client.get(self.url, {"search": "M3"})

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["model"], "M3")

    def test_filter_with_no_match_returns_empty_list(self):
        response = self.client.get(self.url, {"brand": "Ferrari"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])


class VehicleWritePermissionTests(APITestCase):
    """
    Tests dass Schreibzugriffe (POST/PUT/DELETE) nur mit Login
    funktionieren, Lesen (GET) aber immer geht (IsAuthenticatedOrReadOnly).
    """

    url = "/api/vehicles/"

    def setUp(self):
        self.user = User.objects.create_user(
            username="mitarbeiter", password="testpasswort123", role="employee"
        )
        self.payload = {
            "brand": "Mercedes-Benz",
            "model": "C220d",
            "year": 2022,
            "mileage": 12000,
            "price": "35900.00",
            "status": "available",
        }

    def test_create_without_login_is_rejected(self):
        response = self.client.post(self.url, self.payload)

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_create_with_login_succeeds(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(Vehicle.objects.first().brand, "Mercedes-Benz")

    def test_delete_without_login_is_rejected(self):
        vehicle = make_vehicle()

        response = self.client.delete(f"{self.url}{vehicle.id}/")

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertTrue(Vehicle.objects.filter(id=vehicle.id).exists())

    def test_delete_with_login_succeeds(self):
        vehicle = make_vehicle()
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"{self.url}{vehicle.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vehicle.objects.filter(id=vehicle.id).exists())


class VehicleValidationTests(APITestCase):
    """
    Tests für die serverseitige Wertebereichsprüfung: Preis, Baujahr,
    Kilometerstand, Leistung und Türanzahl duerfen keine unsinnigen
    Werte annehmen (z.B. negativer Preis, Baujahr 1500, ...).
    """

    url = "/api/vehicles/"

    def setUp(self):
        self.user = User.objects.create_user(
            username="mitarbeiter3", password="testpasswort123", role="employee"
        )
        self.client.force_authenticate(user=self.user)
        self.base_payload = {
            "brand": "Opel",
            "model": "Astra",
            "year": 2020,
            "mileage": 50000,
            "price": "15900.00",
            "status": "available",
        }

    def test_negative_price_is_rejected(self):
        payload = {**self.base_payload, "price": "-100.00"}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data["details"])

    def test_zero_price_is_rejected(self):
        payload = {**self.base_payload, "price": "0.00"}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data["details"])

    def test_year_too_old_is_rejected(self):
        payload = {**self.base_payload, "year": 1500}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("year", response.data["details"])

    def test_year_too_far_in_future_is_rejected(self):
        payload = {**self.base_payload, "year": 2999}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("year", response.data["details"])

    def test_negative_mileage_is_rejected(self):
        payload = {**self.base_payload, "mileage": -1}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("mileage", response.data["details"])

    def test_unrealistic_mileage_is_rejected(self):
        payload = {**self.base_payload, "mileage": 5_000_000}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("mileage", response.data["details"])

    def test_zero_leistung_is_rejected(self):
        payload = {**self.base_payload, "leistung": 0}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("leistung", response.data["details"])

    def test_unrealistic_leistung_is_rejected(self):
        payload = {**self.base_payload, "leistung": 5000}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("leistung", response.data["details"])

    def test_zero_tueren_is_rejected(self):
        payload = {**self.base_payload, "tueren": 0}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("tueren", response.data["details"])

    def test_too_many_tueren_is_rejected(self):
        payload = {**self.base_payload, "tueren": 20}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("tueren", response.data["details"])

    def test_valid_values_are_accepted(self):
        payload = {
            **self.base_payload,
            "year": 2024,
            "mileage": 0,
            "price": "0.01",
            "leistung": 150,
            "tueren": 5,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_leistung_and_tueren_may_be_omitted(self):
        # Beide Felder sind optional (null=True, blank=True) - ohne Angabe
        # muss das Anlegen trotzdem klappen (Validatoren duerfen nicht auf
        # None angewendet werden).
        response = self.client.post(self.url, self.base_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Vehicle.objects.get(model="Astra")
        self.assertIsNone(created.leistung)
        self.assertIsNone(created.tueren)