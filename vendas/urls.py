from rest_framework.routers import DefaultRouter

from .views import VendaViewSet

router = DefaultRouter()
router.register("", VendaViewSet)

urlpatterns = router.urls
