#!/usr/bin/env python
"""Test MFA functionality"""
import requests
import json

# Login
print("1. Logging in...")
login_response = requests.post('http://127.0.0.1:8000/api/auth/login/', 
    json={'identifier': 'testuser123', 'password': 'password123'})
token = login_response.json()['token']
print(f"✅ Login successful, token: {token[:50]}...")

headers = {'Authorization': f'Bearer {token}'}

# Check MFA status
print("\n2. Checking MFA status...")
status_response = requests.get('http://127.0.0.1:8000/api/auth/mfa/status/', headers=headers)
print(f"✅ MFA Status: {status_response.json()}")

# Setup MFA
print("\n3. Setting up MFA...")
setup_response = requests.post('http://127.0.0.1:8000/api/auth/mfa/setup/', headers=headers)
print(f"Status Code: {setup_response.status_code}")

if setup_response.status_code == 200:
    mfa_data = setup_response.json()
    print(f"✅ MFA Setup successful!")
    print(f"   - Has QR Code: {'qr_code' in mfa_data}")
    print(f"   - QR Code length: {len(mfa_data.get('qr_code', ''))}")
    print(f"   - Has Secret: {'secret' in mfa_data}")
    print(f"   - Secret: {mfa_data.get('secret')}")
    print(f"   - Backup Codes: {len(mfa_data.get('backup_codes', []))} codes")
    for i, code in enumerate(mfa_data.get('backup_codes', [])[:3], 1):
        print(f"      {i}. {code}")
else:
    print(f"❌ Failed: {setup_response.text}")
