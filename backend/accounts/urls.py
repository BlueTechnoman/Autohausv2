#Hier wird festgelegt welcher Code  zu welcher aufgerufenen URL gehört (RH, NW)
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, MeView

urlpatterns = [
    path("register/", RegisterView.as_view()),

    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),

    path("me/", MeView.as_view()),
]