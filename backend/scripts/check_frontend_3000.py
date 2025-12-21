import requests
for u in ['http://localhost:3000/','http://localhost:3000/app-admin/login']:
    try:
        r = requests.get(u, timeout=5)
        print(u, '->', r.status_code, 'len', len(r.text))
    except Exception as e:
        print(u, 'ERROR', e)
