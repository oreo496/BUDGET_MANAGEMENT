from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AIAlertViewSet,
    predict_transaction_type,
    predict_budget_risk,
    predict_goal_success,
    predict_flagged_transaction
)

router = DefaultRouter()
router.register(r'', AIAlertViewSet, basename='aialert')

urlpatterns = [
    path('', include(router.urls)),
    
    # AI Model Prediction Endpoints
    path('predict/transaction/', predict_transaction_type, name='predict-transaction'),
    path('predict/budget-risk/', predict_budget_risk, name='predict-budget-risk'),
    path('predict/goal-success/', predict_goal_success, name='predict-goal-success'),
    path('predict/flagged/', predict_flagged_transaction, name='predict-flagged'),
]

