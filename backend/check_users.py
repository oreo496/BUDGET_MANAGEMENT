#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import User

users = User.objects.all()
print(f'Total users: {users.count()}')
print()
for user in users:
    print(f'Username: {user.username}')
    print(f'Email: {user.email}')
    print(f'Status: {user.status}')
    print(f'ID: {user.id}')
    print('---')
