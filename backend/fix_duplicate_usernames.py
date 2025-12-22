import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from accounts.models import User
from collections import Counter

# Find duplicate usernames
usernames = [(u.id, u.username, u.email) for u in User.objects.all()]
print("Current users:")
for user_id, username, email in usernames:
    print(f"  {user_id} | {username} | {email}")

username_counts = Counter([u[1] for u in usernames])
duplicates = {k: v for k, v in username_counts.items() if v > 1}

if duplicates:
    print(f"\n⚠️ Found duplicates: {duplicates}")
    print("\nFixing duplicate usernames...")
    
    for dup_username in duplicates.keys():
        users_with_dup = User.objects.filter(username=dup_username).order_by('created_at')
        for i, user in enumerate(users_with_dup):
            if i > 0:  # Keep first one, rename others
                new_username = f"{user.email.split('@')[0]}_{i}"
                print(f"  Renaming {user.email}: {user.username} -> {new_username}")
                user.username = new_username
                user.save()
    
    print("\n✅ Fixed all duplicates!")
else:
    print("\n✅ No duplicate usernames found!")

print("\nFinal user list:")
for user in User.objects.all():
    print(f"  {user.username} | {user.email}")
