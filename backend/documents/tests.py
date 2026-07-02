#Hier werden automatisierte Test angelegt mit denen man den Code Prüft

import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from .models import Document

User = get_user_model()

# Test-Uploads landen in einem temporären Ordner statt im echten
# media/-Verzeichnis, damit Testläufe keine Datei-Leichen hinterlassen.
TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix="autohaus_test_media_")


def make_upload(name="vertrag.pdf"):
    return SimpleUploadedFile(name, b"fake-pdf-inhalt", content_type="application/pdf")


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class DocumentVisibilityTests(APITestCase):
    """
    Tests dass Kunden nur ihre eigenen Dokumente sehen,
    Mitarbeiter/Admins aber alle Dokumente.
    """

    url = "/api/documents/"

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

        self.document1 = Document.objects.create(
            customer=self.customer, title="Kaufvertrag",
            document_type="contract", file=make_upload("vertrag1.pdf"),
        )
        self.document2 = Document.objects.create(
            customer=self.other_customer, title="Rechnung",
            document_type="invoice", file=make_upload("rechnung1.pdf"),
        )

    def test_anonymous_cannot_list_documents(self):
        response = self.client.get(self.url)
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_customer_only_sees_own_documents(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [d["id"] for d in response.data]
        self.assertEqual(ids, [self.document1.id])

    def test_employee_sees_all_documents(self):
        self.client.force_authenticate(user=self.employee_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {d["id"] for d in response.data}
        self.assertEqual(ids, {self.document1.id, self.document2.id})


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class DocumentUploadTests(APITestCase):
    """Tests für POST /api/documents/ (Datei-Upload)"""

    url = "/api/documents/"

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="kunde3", password="testpasswort123", role="customer"
        )
        self.customer = Customer.objects.create(
            user=self.customer_user, first_name="Tom", last_name="Test",
            email="tom@example.com", phone="0123456780",
        )

    def test_upload_requires_authentication(self):
        response = self.client.post(self.url, {
            "customer": self.customer.id,
            "title": "Ausweis",
            "document_type": "id_card",
            "file": make_upload("ausweis.pdf"),
        }, format="multipart")

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertEqual(Document.objects.count(), 0)

    def test_upload_with_authentication_succeeds(self):
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(self.url, {
            "customer": self.customer.id,
            "title": "Ausweis",
            "document_type": "id_card",
            "file": make_upload("ausweis.pdf"),
        }, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(Document.objects.first().title, "Ausweis")