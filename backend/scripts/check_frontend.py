import requests

urls = ['http://localhost:3001/', 'http://localhost:3001/app-admin/login']
for u in urls:
    try:
        r = requests.get(u, timeout=5)
        print(u, '->', r.status_code, 'len', len(r.text))
        # show small snippet
        print(r.text[:400].replace('\n',' '))
    except Exception as e:
        print(u, 'ERROR', e)
