import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import User

# Create test user
user = User(
    first_name='Test',
    last_name='User',
    email='user@test.com',
    status='ACTIVE'
)
user.set_password('Test123!')
user.save()

print('✅ User account created successfully!')
print('')
print('=== User Login Credentials ===')
print('Email: user@test.com')
print('Password: Test123!')
print('Login URL: http://localhost:3001/login')
print('==============================')
print('')

# Verify password works
test_user = User.objects.get(email='user@test.com')
if test_user.check_password('Test123!'):
    print('✅ Password verification: SUCCESS')
else:
    print('❌ Password verification: FAILED')
