import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import Admin

EMAIL = os.getenv('APP_ADMIN_EMAIL', 'admin@example.com')
PASSWORD = os.getenv('APP_ADMIN_PASSWORD', 'AdminPass123!')

if Admin.objects.filter(email=EMAIL).exists():
    print(f'App admin {EMAIL} already exists')
else:
    a = Admin(email=EMAIL)
    a.set_password(PASSWORD)
    a.save()
    print(f'Created app admin {EMAIL} with password {PASSWORD}')
