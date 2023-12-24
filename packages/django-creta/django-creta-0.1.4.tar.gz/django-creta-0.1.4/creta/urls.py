from django.urls import path
from rest_framework.routers import DefaultRouter

# App
from creta.views import ApiHistoryViewSet


# Variables
router = DefaultRouter()
router.register(r'histories', ApiHistoryViewSet)
urlpatterns = router.urls

urlpatterns += []
