from django.db import models

# Create your models here.

from customers.models import Customer
from sales.models import Sale

class Document(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, blank=True)

    file = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)