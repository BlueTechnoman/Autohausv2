from django.db import models

# Create your models here.

from django.db import models
from customers.models import Customer
from sales.models import Sale

class Document(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)