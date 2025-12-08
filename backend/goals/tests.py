"""
Tests for goals app.
"""
from django.test import TestCase
from accounts.models import User
from .models import Goal
from decimal import Decimal
from datetime import date, timedelta


class GoalModelTestCase(TestCase):
    """Test cases for Goal model."""
    
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
    
    def test_goal_creation(self):
        """Test creating a goal."""
        goal = Goal.objects.create(
            user=self.user,
            title='Emergency Fund',
            target_amount=Decimal('10000.00'),
            current_amount=Decimal('2500.00'),
            deadline=date.today() + timedelta(days=365)
        )
        
        self.assertEqual(goal.user, self.user)
        self.assertEqual(goal.title, 'Emergency Fund')
        self.assertEqual(goal.target_amount, Decimal('10000.00'))
        self.assertEqual(goal.current_amount, Decimal('2500.00'))
    
    def test_goal_progress_percentage(self):
        """Test goal progress percentage calculation."""
        goal = Goal.objects.create(
            user=self.user,
            title='Vacation',
            target_amount=Decimal('5000.00'),
            current_amount=Decimal('2500.00')
        )
        
        self.assertEqual(goal.progress_percentage, 50.0)
    
    def test_goal_progress_100_percent(self):
        """Test goal at 100% progress."""
        goal = Goal.objects.create(
            user=self.user,
            title='Completed Goal',
            target_amount=Decimal('1000.00'),
            current_amount=Decimal('1500.00')  # Exceeds target
        )
        
        # Should cap at 100%
        self.assertEqual(goal.progress_percentage, 100.0)
    
    def test_goal_uuid_string(self):
        """Test goal UUID string conversion."""
        goal = Goal.objects.create(
            user=self.user,
            title='Test Goal',
            target_amount=Decimal('1000.00')
        )
        
        uuid_str = goal.get_uuid_string()
        self.assertIsInstance(uuid_str, str)
        self.assertEqual(len(uuid_str), 36)

