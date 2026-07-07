#Hier werden automatisierte Test angelegt mit denen man den Code Prüft
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterTests(APITestCase):
    """Tests für POST /api/accounts/register/"""

    url = "/api/accounts/register/"

    def test_register_creates_customer(self):
        """Normale Registrierung legt einen User mit role=customer an."""
        response = self.client.post(self.url, {
            "username": "maxmustermann",
            "email": "max@example.com",
            "password": "sehr-sicheres-passwort-123",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["role"], "customer")

        user = User.objects.get(username="maxmustermann")
        self.assertEqual(user.role, "customer")
        # Passwort darf niemals im Klartext gespeichert sein
        self.assertNotEqual(user.password, "sehr-sicheres-passwort-123")
        self.assertTrue(user.check_password("sehr-sicheres-passwort-123"))

    def test_register_cannot_escalate_role_to_admin(self):
        """
        Regressionstest für die role-Sicherheitslücke:
        Ein Client darf sich NICHT selbst role="admin" geben können,
        egal was im Request-Body steht.
        """
        response = self.client.post(self.url, {
            "username": "hacker",
            "email": "hacker@example.com",
            "password": "sehr-sicheres-passwort-123",
            "role": "admin",
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["role"], "customer")

        user = User.objects.get(username="hacker")
        self.assertEqual(user.role, "customer")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_register_missing_password_fails(self):
        response = self.client.post(self.url, {
            "username": "ohnepasswort",
            "email": "test@example.com",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="ohnepasswort").exists())

    def test_register_duplicate_username_fails(self):
        User.objects.create_user(username="doppelt", password="testpasswort123")

        response = self.client.post(self.url, {
            "username": "doppelt",
            "email": "andere@example.com",
            "password": "testpasswort123",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_too_short_fails(self):
        response = self.client.post(self.url, {
            "username": "kurzespw",
            "email": "kurz@example.com",
            "password": "abc123",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data["details"])
        self.assertFalse(User.objects.filter(username="kurzespw").exists())

    def test_register_common_password_fails(self):
        response = self.client.post(self.url, {
            "username": "haeufigespw",
            "email": "haeufig@example.com",
            "password": "password123",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data["details"])

    def test_register_numeric_only_password_fails(self):
        response = self.client.post(self.url, {
            "username": "numerischespw",
            "email": "numerisch@example.com",
            "password": "48291736450",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data["details"])

    def test_register_password_similar_to_username_fails(self):
        response = self.client.post(self.url, {
            "username": "sonderbarername123",
            "email": "aehnlich@example.com",
            "password": "sonderbarername123",
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data["details"])


class LoginTests(APITestCase):
    """Tests für POST /api/accounts/login/ (JWT)"""

    url = "/api/accounts/login/"

    def setUp(self):
        self.user = User.objects.create_user(
            username="loginuser",
            password="korrektesPasswort123",
            role="customer",
        )

    def test_login_with_correct_credentials_returns_tokens(self):
        response = self.client.post(self.url, {
            "username": "loginuser",
            "password": "korrektesPasswort123",
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(self.url, {
            "username": "loginuser",
            "password": "falschesPasswort",
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_unknown_user_fails(self):
        response = self.client.post(self.url, {
            "username": "gibtsnicht",
            "password": "irgendwas123",
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MeViewTests(APITestCase):
    """Tests für GET /api/accounts/me/"""

    url = "/api/accounts/me/"

    def setUp(self):
        self.user = User.objects.create_user(
            username="meuser",
            email="me@example.com",
            password="testpasswort123",
            role="customer",
        )

    def test_me_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_current_user_data(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "meuser")
        self.assertEqual(response.data["email"], "me@example.com")
        self.assertEqual(response.data["role"], "customer")