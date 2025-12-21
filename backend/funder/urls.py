"""
URL configuration for funder project.
"""
from django.contrib import admin
from django.urls import path, include
from funder.views import health_check, predict_transaction, predict_transaction_test

urlpatterns = [
    # Health check endpoints
    path('', health_check, name='health'),
    path('health/', health_check, name='health'),
    path('api/health/', health_check, name='api-health'),
    
    # AI Prediction endpoints
    path('api/predict/', predict_transaction, name='predict-transaction'),
    path('api/predict/test/', predict_transaction_test, name='predict-test'),
    
    # Admin and app routes
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/users/', include('accounts.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/loans/', include('loans.urls')),
    path('api/budgets/', include('budgets.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/bank-accounts/', include('bank_accounts.urls')),
    path('api/ai-alerts/', include('ai_alerts.urls')),
    path('api/admin/', include('admin_panel.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]

