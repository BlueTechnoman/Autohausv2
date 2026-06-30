#Hier wird festgelegt welcher Code  zu welcher aufgerufenen URL gehört (RH, NW)

from django.urls import path
from .views import DashboardView

urlpatterns = [
    path("dashboard/", DashboardView.as_view()),
]