"""
Pytest configuration and fixtures.
"""
import pytest
from accounts.models import User, Admin
from categories.models import Category
from transactions.models import Transaction
from budgets.models import Budget
from goals.models import Goal
from decimal import Decimal
from datetime import date, timedelta


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User.objects.create(
        first_name='Test',
        last_name='User',
        email='test@example.com',
        status='ACTIVE'
    )
    user.set_password('testpass123')
    user.save()
    return user


@pytest.fixture
def test_admin(db):
    """Create a test admin."""
    admin = Admin.objects.create(
        email='admin@example.com'
    )
    admin.set_password('adminpass123')
    admin.save()
    return admin


@pytest.fixture
def test_category(db, test_user):
    """Create a test category."""
    return Category.objects.create(
        user=test_user,
        name='Groceries',
        type='EXPENSE'
    )


@pytest.fixture
def test_transaction(db, test_user, test_category):
    """Create a test transaction."""
    return Transaction.objects.create(
        user=test_user,
        category=test_category,
        amount=Decimal('100.00'),
        type='EXPENSE',
        merchant='Test Store',
        date=date.today(),
        source='MANUAL'
    )


@pytest.fixture
def test_budget(db, test_user, test_category):
    """Create a test budget."""
    return Budget.objects.create(
        user=test_user,
        category=test_category,
        period='MONTHLY',
        amount=Decimal('1000.00')
    )


@pytest.fixture
def test_goal(db, test_user):
    """Create a test goal."""
    return Goal.objects.create(
        user=test_user,
        title='Test Goal',
        target_amount=Decimal('5000.00'),
        current_amount=Decimal('1000.00'),
        deadline=date.today() + timedelta(days=180)
    )

