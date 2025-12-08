from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemLogViewSet, AdminActionViewSet

router = DefaultRouter()
router.register(r'logs', SystemLogViewSet, basename='systemlog')
router.register(r'actions', AdminActionViewSet, basename='adminaction')

urlpatterns = [
    path('', include(router.urls)),
]

