"""
Tests for accounts app.
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Admin


class UserModelTestCase(TestCase):
    """Test cases for User model."""
    
    def test_user_creation(self):
        """Test creating a user."""
        user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            status='ACTIVE'
        )
        user.set_password('testpassword123')
        user.save()
        
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertFalse(user.check_password('wrongpassword'))
        self.assertEqual(user.status, 'ACTIVE')
    
    def test_user_uuid_string(self):
        """Test UUID string conversion."""
        user = User.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com'
        )
        user.set_password('password')
        user.save()
        
        uuid_str = user.get_uuid_string()
        self.assertIsInstance(uuid_str, str)
        self.assertEqual(len(uuid_str), 36)  # UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    
    def test_user_password_hashing(self):
        """Test that passwords are properly hashed."""
        user = User.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com'
        )
        user.set_password('plainpassword')
        user.save()
        
        # Password should be hashed, not stored as plain text
        self.assertNotEqual(user.password_hash, 'plainpassword')
        self.assertTrue(user.password_hash.startswith('$2b$'))  # bcrypt hash format


class UserAPITestCase(TestCase):
    """Test cases for User API endpoints."""
    
    def setUp(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user = User.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            status='ACTIVE'
        )
        self.user.set_password('testpass123')
        self.user.save()
    
    def test_register_user(self):
        """Test user registration endpoint."""
        url = reverse('register')
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'phone': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')
    
    def test_register_duplicate_email(self):
        """Test that duplicate email registration fails."""
        url = reverse('register')
        data = {
            'first_name': 'Duplicate',
            'last_name': 'User',
            'email': 'test@example.com',  # Already exists
            'password': 'pass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_success(self):
        """Test successful login."""
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user."""
        url = reverse('login')
        data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminModelTestCase(TestCase):
    """Test cases for Admin model."""
    
    def test_admin_creation(self):
        """Test creating an admin."""
        admin = Admin.objects.create(
            email='admin@example.com'
        )
        admin.set_password('adminpass123')
        admin.save()
        
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertTrue(admin.check_password('adminpass123'))
        self.assertFalse(admin.check_password('wrongpassword'))
    
    def test_admin_uuid_string(self):
        """Test admin UUID string conversion."""
        admin = Admin.objects.create(
            email='admin@example.com'
        )
        admin.set_password('password')
        admin.save()
        
        uuid_str = admin.get_uuid_string()
        self.assertIsInstance(uuid_str, str)
        self.assertEqual(len(uuid_str), 36)
