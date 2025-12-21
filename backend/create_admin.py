import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import Admin

# Create admin properly
admin = Admin(email='admin@funder.com')
admin.set_password('admin123')
admin.save()

print('✅ Admin account created successfully!')
print('')
print('=== Admin Login Credentials ===')
print('Email: admin@funder.com')
print('Password: admin123')
print('URL: http://localhost:3000/admin')
print('===============================')
print('')

# Verify it works
test_admin = Admin.objects.get(email='admin@funder.com')
if test_admin.check_password('admin123'):
    print('✅ Password verification: SUCCESS')
else:
    print('❌ Password verification: FAILED')
