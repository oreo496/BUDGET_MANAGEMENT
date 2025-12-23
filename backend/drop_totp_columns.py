#!/usr/bin/env python
"""
Drop TOTP columns from the users table.
Run with: python drop_totp_columns.py
"""
import os
import django
import sys

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from django.db import connection

def drop_columns():
    with connection.cursor() as cursor:
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN two_factor_enabled")
            print("✓ two_factor_enabled column dropped successfully")
        except Exception as e:
            print(f"✗ Error dropping two_factor_enabled: {e}")
        
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN two_factor_secret")
            print("✓ two_factor_secret column dropped successfully")
        except Exception as e:
            print(f"✗ Error dropping two_factor_secret: {e}")
        
        try:
            cursor.execute("ALTER TABLE users DROP COLUMN backup_codes")
            print("✓ backup_codes column dropped successfully")
        except Exception as e:
            print(f"✗ Error dropping backup_codes: {e}")

if __name__ == '__main__':
    drop_columns()
