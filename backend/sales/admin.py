#Führt beim Start der Anwendung dazu das Initialisierungscode ausgeführt wird (RH, NW)

from django.contrib import admin
from .models import Sale

admin.site.register(Sale)