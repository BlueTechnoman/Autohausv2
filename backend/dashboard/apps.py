#Führt beim Start der Anwendung dazu das Initialisierungscode ausgeführt wird (RH, NW)

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'
