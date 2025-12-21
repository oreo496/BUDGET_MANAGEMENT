import requests
import sys

BASE = 'http://127.0.0.1:8000'

def register():
    try:
        r = requests.post(f'{BASE}/api/auth/register/', json={
            'email': 'user@example.com',
            'password': 'UserPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        })
        print('REGISTER', r.status_code, r.text)
    except Exception as e:
        print('REGISTER ERROR', e)

def login_user():
    try:
        r = requests.post(f'{BASE}/api/auth/login/', json={'email':'user@example.com','password':'UserPass123!'})
        print('USER LOGIN', r.status_code, r.text)
        if r.status_code==200:
            return r.json().get('token')
    except Exception as e:
        print('LOGIN ERROR', e)
    return None

def profile(token):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.get(f'{BASE}/api/auth/profile/', headers=headers)
        print('PROFILE', r.status_code, r.text)
    except Exception as e:
        print('PROFILE ERROR', e)

def admin_login():
    try:
        r = requests.post(f'{BASE}/api/admin/auth/login/', json={'email':'admin@example.com','password':'AdminPass123!'})
        print('ADMIN LOGIN', r.status_code, r.text)
        if r.status_code==200:
            return r.json().get('token')
    except Exception as e:
        print('ADMIN LOGIN ERROR', e)
    return None

if __name__=='__main__':
    register()
    tok = login_user()
    if tok:
        profile(tok)
    admin_login()
