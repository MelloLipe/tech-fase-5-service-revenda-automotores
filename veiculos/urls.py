from rest_framework.routers import DefaultRouter

from .views import VeiculoViewSet

router = DefaultRouter()
router.register("", VeiculoViewSet)

urlpatterns = router.urls
