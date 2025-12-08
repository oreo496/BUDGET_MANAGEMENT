from django.urls import path
from . import views
from . import mfa_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    # MFA endpoints
    path('mfa/setup/', mfa_views.setup_mfa, name='mfa_setup'),
    path('mfa/verify-setup/', mfa_views.verify_mfa_setup, name='mfa_verify_setup'),
    path('mfa/disable/', mfa_views.disable_mfa, name='mfa_disable'),
    path('mfa/status/', mfa_views.get_mfa_status, name='mfa_status'),
]

