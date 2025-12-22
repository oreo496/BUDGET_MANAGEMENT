import pytest
from decimal import Decimal
from datetime import date, timedelta
from rest_framework.test import APIClient
from accounts.models import User
from transactions.models import Transaction
from goals.models import Goal
from utils.jwt_auth import generate_token


@pytest.mark.django_db
def test_goal_insights_endpoint_returns_200(test_user):
    # Create a goal
    goal = Goal.objects.create(
        user=test_user,
        title='Vacation Fund',
        target_amount=Decimal('3000.00'),
        current_amount=Decimal('500.00'),
        deadline=date.today() + timedelta(days=90)
    )

    # Create recent transactions (last 30 days)
    Transaction.objects.create(
        user=test_user,
        amount=Decimal('2000.00'),
        type='INCOME',
        date=date.today() - timedelta(days=10)
    )
    Transaction.objects.create(
        user=test_user,
        amount=Decimal('600.00'),
        type='EXPENSE',
        date=date.today() - timedelta(days=5)
    )

    # Auth token
    token = generate_token(test_user)
    client = APIClient()
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    # Call insights
    url = f'/api/goals/{goal.get_uuid_string()}/insights/'
    response = client.post(url)

    assert response.status_code == 200
    data = response.json()
    assert 'progress_percentage' in data
    assert 'monthly_surplus' in data
    assert 'required_monthly' in data
    assert 'risk' in data
    assert 'days_left' in data


@pytest.mark.django_db
def test_goal_insights_handles_errors_gracefully(test_user):
    # Create a goal with zero target to test edge
    goal = Goal.objects.create(
        user=test_user,
        title='Edge Goal',
        target_amount=Decimal('0.00'),
        current_amount=Decimal('0.00')
    )

    token = generate_token(test_user)
    client = APIClient()
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    url = f'/api/goals/{goal.get_uuid_string()}/insights/'
    response = client.post(url)

    # Should still succeed and not 500
    assert response.status_code in (200, 400)
