import os
import django
import bcrypt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import Admin

# Get admin
admin = Admin.objects.get(email='admin@funder.com')
print('Admin email:', admin.email)
print('Password hash from DB:', admin.password_hash)
print('Hash length:', len(admin.password_hash))

# Test password
test_password = 'admin123'
print('\nTesting password:', test_password)

# Test using model method
result = admin.check_password(test_password)
print('Model check_password result:', result)

# Test bcrypt directly
print('\nTesting bcrypt directly...')
try:
    direct_result = bcrypt.checkpw(
        test_password.encode('utf-8'),
        admin.password_hash.encode('utf-8')
    )
    print('Direct bcrypt result:', direct_result)
except Exception as e:
    print('Error:', e)

# Create a new hash and test it
print('\nCreating fresh hash...')
new_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
print('New hash:', new_hash)
new_hash_str = new_hash.decode('utf-8')
print('New hash (decoded):', new_hash_str)

# Test the new hash
fresh_check = bcrypt.checkpw(test_password.encode('utf-8'), new_hash)
print('Fresh hash check:', fresh_check)

# Update admin with new hash
print('\nUpdating admin password...')
admin.set_password(test_password)
Admin.objects.filter(id=admin.id).update(password_hash=admin.password_hash)
print('Password updated!')

# Verify update
admin.refresh_from_db()
print('New hash in DB:', admin.password_hash)
final_result = admin.check_password(test_password)
print('Final verification:', final_result)
