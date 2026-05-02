from rest_framework.routers import DefaultRouter

from .views import CompradorViewSet

router = DefaultRouter()
router.register("", CompradorViewSet)

urlpatterns = router.urls
