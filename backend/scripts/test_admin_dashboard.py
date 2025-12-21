import requests

BASE='http://127.0.0.1:8000'

try:
    r = requests.post(f'{BASE}/api/admin/auth/login/', json={'email':'admin@example.com','password':'AdminPass123!'}, timeout=5)
    print('LOGIN', r.status_code, r.text)
    if r.status_code==200:
        token = r.json().get('token')
        r2 = requests.get(f'{BASE}/api/admin/dashboard/', headers={'Authorization': f'Bearer {token}'}, timeout=5)
        print('DASH', r2.status_code, r2.text)
    else:
        print('login failed')
except Exception as e:
    print('ERROR', e)
