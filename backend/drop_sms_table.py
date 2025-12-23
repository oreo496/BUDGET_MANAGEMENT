#!/usr/bin/env python
"""
Drop the sms_otps table from the database.
Run with: python drop_sms_table.py
"""
import os
import django
import sys

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
django.setup()

from django.db import connection

def drop_table():
    with connection.cursor() as cursor:
        try:
            cursor.execute("DROP TABLE IF EXISTS sms_otps")
            print("✓ sms_otps table dropped successfully")
        except Exception as e:
            print(f"✗ Error dropping table: {e}")
            sys.exit(1)

if __name__ == '__main__':
    drop_table()
