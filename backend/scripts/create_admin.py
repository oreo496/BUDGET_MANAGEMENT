import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from django.contrib.auth.models import User

USERNAME = os.getenv('DJANGO_ADMIN_USERNAME', 'admin')
EMAIL = os.getenv('DJANGO_ADMIN_EMAIL', 'admin@example.com')
PASSWORD = os.getenv('DJANGO_ADMIN_PASSWORD', 'AdminPass123!')

if User.objects.filter(username=USERNAME).exists():
    print(f'Superuser "{USERNAME}" already exists')
else:
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print(f'Created superuser "{USERNAME}" with password "{PASSWORD}"')
