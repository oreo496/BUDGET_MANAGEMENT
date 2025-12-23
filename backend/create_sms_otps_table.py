"""Create SMS OTP table without foreign key."""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funder.settings')
import django
django.setup()

from django.db import connection
with connection.cursor() as cursor:
    sql = """CREATE TABLE IF NOT EXISTS sms_otps (
        id BINARY(16) PRIMARY KEY,
        user_id BINARY(16) NOT NULL,
        code VARCHAR(6) NOT NULL,
        attempts INT NOT NULL DEFAULT 0,
        max_attempts INT NOT NULL DEFAULT 3,
        created_at DATETIME(6) NOT NULL,
        expires_at DATETIME(6) NOT NULL,
        KEY user_id_idx (user_id),
        KEY expires_at_idx (expires_at)
    );"""
    try:
        cursor.execute(sql)
        print("SMS OTP table created successfully.")
    except Exception as e:
        if "already exists" in str(e):
            print("SMS OTP table already exists.")
        else:
            print(f"Error: {e}")
