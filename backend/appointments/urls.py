#Hier wird festgelegt welcher Code  zu welcher aufgerufenen URL gehört (RH, NW)
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet

router = DefaultRouter()
router.register(
    r"appointments",
    AppointmentViewSet
)

urlpatterns = router.urls