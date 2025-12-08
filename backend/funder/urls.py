"""
URL configuration for funder project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint."""
    return JsonResponse({'status': 'ok', 'message': 'Funder API is running'})

urlpatterns = [
    path('', health_check, name='health'),
    path('health/', health_check, name='health'),
    path('api/health/', health_check, name='api-health'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/users/', include('accounts.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/budgets/', include('budgets.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/bank-accounts/', include('bank_accounts.urls')),
    path('api/ai-alerts/', include('ai_alerts.urls')),
    path('api/admin/', include('admin_panel.urls')),
]

