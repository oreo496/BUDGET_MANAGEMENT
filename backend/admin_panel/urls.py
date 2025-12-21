from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemLogViewSet, AdminActionViewSet
from . import views

router = DefaultRouter()
router.register(r'logs', SystemLogViewSet, basename='systemlog')
router.register(r'actions', AdminActionViewSet, basename='adminaction')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', views.admin_login, name='admin-login'),
    path('auth/logout/', views.admin_logout, name='admin-logout'),
    path('dashboard/', views.dashboard, name='admin-dashboard'),
    path('users/', views.list_users, name='admin-list-users'),
    path('users/<str:user_id>/toggle/', views.toggle_user_status, name='admin-toggle-user'),
    path('users/<str:user_id>/delete/', views.delete_user, name='admin-delete-user'),
    path('system/stats/', views.system_stats, name='admin-system-stats'),
]

