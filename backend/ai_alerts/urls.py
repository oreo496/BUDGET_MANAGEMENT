from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIAlertViewSet

router = DefaultRouter()
router.register(r'', AIAlertViewSet, basename='aialert')

urlpatterns = [
    path('', include(router.urls)),
]

