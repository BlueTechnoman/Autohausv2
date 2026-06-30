#Hier wird festgelegt welcher Code  zu welcher aufgerufenen URL gehört (RH, NW)


from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, VehicleImageViewSet

router = DefaultRouter()

router.register(
    r"vehicles",
    VehicleViewSet
)

router.register(
    r"vehicle-images",
    VehicleImageViewSet
)

urlpatterns = router.urls