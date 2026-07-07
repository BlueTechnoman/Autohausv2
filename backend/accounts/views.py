#Hier wird die Logik der Anwendung festgelegt. Eine View verarbeitet eine Anfrage, 
#führt dann den benötigten Code aus und gibt eine Antwort (RH, NW)

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer

User = get_user_model()


# -------------------------
# REGISTER
# -------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------
# ME (aktueller User)
# -------------------------
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        })