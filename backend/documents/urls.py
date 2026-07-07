#Hier wird festgelegt welcher Code  zu welcher aufgerufenen URL gehört (RH, NW)

from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet

router = DefaultRouter()

router.register(
    r"documents",
    DocumentViewSet,
    basename="documents"
)

urlpatterns = router.urls