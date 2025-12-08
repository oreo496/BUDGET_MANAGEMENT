"""
Tests for budgets app.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from categories.models import Category
from .models import Budget
from decimal import Decimal


class BudgetModelTestCase(TestCase):
    """Test cases for Budget model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            status='ACTIVE'
        )
        self.user.set_password('testpass')
        self.user.save()
        
        self.category = Category.objects.create(
            user=self.user,
            name='Groceries',
            type='EXPENSE'
        )
    
    def test_budget_creation(self):
        """Test creating a budget."""
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            period='MONTHLY',
            amount=Decimal('1000.00')
        )
        
        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.category, self.category)
        self.assertEqual(budget.period, 'MONTHLY')
        self.assertEqual(budget.amount, Decimal('1000.00'))
    
    def test_budget_uuid_string(self):
        """Test budget UUID string conversion."""
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            period='WEEKLY',
            amount=Decimal('250.00')
        )
        
        uuid_str = budget.get_uuid_string()
        self.assertIsInstance(uuid_str, str)
        self.assertEqual(len(uuid_str), 36)
    
    def test_budget_non_negative_amount(self):
        """Test that budget amount cannot be negative."""
        from django.db import IntegrityError
        
        with self.assertRaises(IntegrityError):
            Budget.objects.create(
                user=self.user,
                category=self.category,
                period='MONTHLY',
                amount=Decimal('-100.00')
            )

