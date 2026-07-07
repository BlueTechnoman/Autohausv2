#Registriert Modelle im Django-Adminbereich und macht es verwendbar (RH, NW)
from django.contrib import admin
from .models import Customer

admin.site.register(Customer)