#Hier wird die Logik der Anwendung festgelegt. Eine View verarbeitet eine Anfrage, 
#führt dann den benötigten Code aus und gibt eine Antwort (RH, NW)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()   # WICHTIG
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "customer":
            return Document.objects.filter(
                customer__user=user
            )

        return Document.objects.all()