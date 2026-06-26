from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import VehicleViewSet, VehicleImageViewSet, proxy_image

router = DefaultRouter()
router.register(r"vehicles",       VehicleViewSet)
router.register(r"vehicle-images", VehicleImageViewSet)

urlpatterns = router.urls + [
    path("proxy-image/", proxy_image, name="proxy-image"),
]