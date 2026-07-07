#Registriert Modelle im Django-Adminbereich und macht es verwendbar (RH, NW)
from django.contrib import admin
from .models import Appointment

admin.site.register(Appointment)