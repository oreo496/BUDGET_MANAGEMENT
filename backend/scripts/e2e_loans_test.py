import requests
import uuid
import time

BASE = 'http://127.0.0.1:8000/api'

def main():
    rid = str(uuid.uuid4())[:8]
    email = f'test_{rid}@example.com'
    password = 'TestPass123!'

    print('Registering user:', email)
    r = requests.post(f'{BASE}/auth/register/', json={
        'first_name': 'E2E',
        'last_name': 'Tester',
        'email': email,
        'password': password
    })
    print('Register status:', r.status_code, r.text)

    print('\nLogging in')
    r = requests.post(f'{BASE}/auth/login/', json={'email': email, 'password': password})
    print('Login status:', r.status_code, r.text)
    if r.status_code != 200:
        print('Login failed — aborting')
        return
    token = r.json().get('token')
    headers = {'Authorization': f'Bearer {token}'}

    print('\nCreating a loan')
    r = requests.post(f'{BASE}/loans/', json={'amount': 2500.00, 'term_months': 12, 'interest_rate': 4.5}, headers=headers)
    print('Create loan status:', r.status_code, r.text)

    print('\nListing loans')
    r = requests.get(f'{BASE}/loans/', headers=headers)
    print('List loans status:', r.status_code, r.text)

if __name__ == '__main__':
    main()
