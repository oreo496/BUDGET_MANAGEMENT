"""
Integration tests for the Funder application.
"""
import pytest
from django.test import Client
from django.urls import reverse
from accounts.models import User
from transactions.models import Transaction
from budgets.models import Budget
from goals.models import Goal
from categories.models import Category
from decimal import Decimal
from datetime import date


@pytest.mark.django_db
class TestUserWorkflow:
    """Test complete user workflow."""
    
    def test_user_registration_and_transaction_flow(self, test_user, test_category):
        """Test user can register and create transactions."""
        # User is already created via fixture
        assert User.objects.filter(email='test@example.com').exists()
        
        # Create a transaction
        transaction = Transaction.objects.create(
            user=test_user,
            category=test_category,
            amount=Decimal('50.00'),
            type='EXPENSE',
            merchant='Test Merchant',
            date=date.today()
        )
        
        assert transaction.user == test_user
        assert transaction.amount == Decimal('50.00')
        assert Transaction.objects.filter(user=test_user).count() == 1
    
    def test_budget_and_goal_creation(self, test_user, test_category):
        """Test user can create budgets and goals."""
        # Create budget
        budget = Budget.objects.create(
            user=test_user,
            category=test_category,
            period='MONTHLY',
            amount=Decimal('1000.00')
        )
        
        # Create goal
        goal = Goal.objects.create(
            user=test_user,
            title='Emergency Fund',
            target_amount=Decimal('10000.00'),
            current_amount=Decimal('2500.00')
        )
        
        assert Budget.objects.filter(user=test_user).count() == 1
        assert Goal.objects.filter(user=test_user).count() == 1
        assert goal.progress_percentage == 25.0


@pytest.mark.django_db
class TestDataIntegrity:
    """Test data integrity and constraints."""
    
    def test_user_cascade_delete(self, test_user, test_category):
        """Test that deleting user cascades to related data."""
        # Create related data
        Transaction.objects.create(
            user=test_user,
            category=test_category,
            amount=Decimal('100.00'),
            type='EXPENSE',
            date=date.today()
        )
        Budget.objects.create(
            user=test_user,
            category=test_category,
            period='MONTHLY',
            amount=Decimal('500.00')
        )
        Goal.objects.create(
            user=test_user,
            title='Test Goal',
            target_amount=Decimal('1000.00')
        )
        
        user_id = test_user.id
        test_user.delete()
        
        # All related data should be deleted
        assert not Transaction.objects.filter(user_id=user_id).exists()
        assert not Budget.objects.filter(user_id=user_id).exists()
        assert not Goal.objects.filter(user_id=user_id).exists()
        # Category should also be deleted (CASCADE)
        assert not Category.objects.filter(user_id=user_id).exists()

