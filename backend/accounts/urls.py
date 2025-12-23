from django.urls import path
from . import views
from . import mfa_views
from . import sms_otp_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    # MFA endpoints
    path('mfa/setup/', mfa_views.setup_mfa, name='mfa_setup'),
    path('mfa/verify-setup/', mfa_views.verify_mfa_setup, name='mfa_verify_setup'),
    path('mfa/disable/', mfa_views.disable_mfa, name='mfa_disable'),
    path('mfa/status/', mfa_views.get_mfa_status, name='mfa_status'),
    # SMS OTP endpoints
    path('sms-otp/request/', sms_otp_views.request_sms_otp, name='request_sms_otp'),
    path('sms-otp/verify/', sms_otp_views.verify_sms_otp, name='verify_sms_otp'),
    path('sms-otp/setup/', sms_otp_views.setup_sms_otp, name='setup_sms_otp'),
    path('sms-otp/disable/', sms_otp_views.disable_sms_otp, name='disable_sms_otp'),
]

