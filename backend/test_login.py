#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import User
from utils.security import sanitize_input, validate_email

# Test with one of the existing users
identifier = "user_2"  # or try "user@example.com"
print(f"Testing login with identifier: {identifier}")

# Simulate what the backend does
username_or_email = sanitize_input(identifier, max_length=100)
print(f"After sanitization: {username_or_email}")

try:
    if '@' in username_or_email:
        print("Looking up by email...")
        user = User.objects.get(email=validate_email(username_or_email))
    else:
        print("Looking up by username...")
        user = User.objects.get(username=username_or_email)
    
    print(f"✓ User found: {user.username} ({user.email})")
    print(f"  Status: {user.status}")
    print(f"  ID: {user.id}")
except User.DoesNotExist:
    print("✗ User not found")
except Exception as e:
    print(f"✗ Error: {e}")
