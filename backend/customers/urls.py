#Hier wird festgelegt welcher Code  zu welcher aufgerufenen URL gehört (RH, NW)

from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = router.urls