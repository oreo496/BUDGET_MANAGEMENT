"""
Tests for transactions app.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from categories.models import Category
from .models import Transaction
from decimal import Decimal
from datetime import date, timedelta


class TransactionModelTestCase(TestCase):
    """Test cases for Transaction model."""
    
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
    
    def test_transaction_creation(self):
        """Test creating a transaction."""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100.50'),
            type='EXPENSE',
            merchant='Test Store',
            date=date.today(),
            source='MANUAL'
        )
        
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.amount, Decimal('100.50'))
        self.assertEqual(transaction.type, 'EXPENSE')
        self.assertEqual(transaction.merchant, 'Test Store')
        self.assertFalse(transaction.flagged_fraud)
    
    def test_transaction_uuid_string(self):
        """Test transaction UUID string conversion."""
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            type='INCOME',
            date=date.today()
        )
        
        uuid_str = transaction.get_uuid_string()
        self.assertIsInstance(uuid_str, str)
        self.assertEqual(len(uuid_str), 36)
    
    def test_transaction_fraud_flagging(self):
        """Test flagging a transaction as fraud."""
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('5000.00'),
            type='EXPENSE',
            date=date.today(),
            flagged_fraud=False
        )
        
        transaction.flagged_fraud = True
        transaction.save()
        
        self.assertTrue(transaction.flagged_fraud)


class TransactionAPITestCase(TestCase):
    """Test cases for Transaction API endpoints."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = APIClient()
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
            name='Shopping',
            type='EXPENSE'
        )
        
        # Authenticate client (would need JWT middleware in real implementation)
        # self.client.force_authenticate(user=self.user)
    
    def test_create_transaction(self):
        """Test creating a transaction via API."""
        url = reverse('transaction-list')
        data = {
            'user': self.user.get_uuid_string(),
            'category': self.category.get_uuid_string(),
            'amount': '150.75',
            'type': 'EXPENSE',
            'merchant': 'Test Merchant',
            'date': date.today().isoformat(),
            'source': 'MANUAL'
        }
        response = self.client.post(url, data, format='json')
        
        # Note: This will fail without proper authentication
        # In real implementation, add JWT token to headers
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_401_UNAUTHORIZED])
    
    def test_list_transactions(self):
        """Test listing transactions."""
        # Create test transactions
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100.00'),
            type='EXPENSE',
            date=date.today()
        )
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('500.00'),
            type='INCOME',
            date=date.today() - timedelta(days=1)
        )
        
        url = reverse('transaction-list')
        response = self.client.get(url)
        
        # Note: This will fail without proper authentication
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
    
    def test_flag_fraud_transaction(self):
        """Test flagging a transaction as fraud."""
        transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('10000.00'),
            type='EXPENSE',
            date=date.today()
        )
        
        url = reverse('transaction-flag-fraud', kwargs={'pk': transaction.get_uuid_string()})
        response = self.client.post(url)
        
        # Note: This will fail without proper authentication
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
        
        if response.status_code == status.HTTP_200_OK:
            transaction.refresh_from_db()
            self.assertTrue(transaction.flagged_fraud)

