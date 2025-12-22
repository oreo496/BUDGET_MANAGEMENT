import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

# Add testserver to allowed hosts for testing
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from goals.models import Goal
from django.test import Client
from utils.jwt_auth import generate_token

goal = Goal.objects.first()
user = goal.user

print(f'Testing endpoint with Goal: {goal.title}')
print(f'User: {user.email}')
print()

# Create a test client
client = Client()
token = generate_token(user)

# Call the insights endpoint
url = f'/api/goals/{goal.get_uuid_string()}/insights/'
response = client.post(url, HTTP_AUTHORIZATION=f'Bearer {token}')

print(f'Response Status: {response.status_code}')
try:
    print(f'Response Data: {response.json()}')
except:
    print(f'Response Text: {response.content}')

if response.status_code == 200:
    print('\n✓ SUCCESS - Insights endpoint works!')
elif response.status_code >= 500:
    print(f'\n✗ FAILED - Got server error {response.status_code}')
else:
    print(f'\nWarning - Got status {response.status_code}')


