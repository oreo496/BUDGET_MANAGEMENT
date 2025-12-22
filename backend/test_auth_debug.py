"""Debug script to test JWT authentication"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import User
from django.conf import settings
import jwt

# Get first user
user = User.objects.first()
if not user:
    print("No users found!")
    exit(1)

print(f"User ID: {user.id}")
print(f"User ID type: {type(user.id)}")
print(f"User ID string: {user.get_uuid_string()}")
print(f"User email: {user.email}")

# Create token like login does
token = jwt.encode({
    'user_id': user.get_uuid_string(),
    'email': user.email,
}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

print(f"\nGenerated token: {token}")

# Decode it back
payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
print(f"\nDecoded payload: {payload}")
print(f"user_id from payload: {payload['user_id']}")
print(f"user_id type: {type(payload['user_id'])}")

# Try to query with it
user_id = payload.get('user_id')
try:
    found_user = User.objects.get(id=user_id)
    print(f"\n✓ SUCCESS: Found user: {found_user.email}")
except User.DoesNotExist:
    print(f"\n✗ ERROR: User not found with id={user_id}")
    print(f"\nTrying to find user manually:")
    all_users = User.objects.all()
    for u in all_users:
        print(f"  - {u.id} ({type(u.id)}) - {u.email}")
        if str(u.id) == user_id:
            print(f"    ✓ String match found!")
