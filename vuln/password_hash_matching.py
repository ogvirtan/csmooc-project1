import hashlib
import time

password_hash = 'md5$HegexxEdibs99ZdATmoNHZ$96b0800a0389362bb366af6387ce1f09'
alg, salt, stored_hash = password_hash.split('$')

#Creating a password list of over a million entries
passwords = ['pad'] * 100000
entries = [
    'password',
    'password123',
    'pass123word',
    '4123',
    '3412',
    '2341',
    '1234',
    '12345',
    'asd',
    'asdasd'
]
passwords.extend(entries)

start_md5 = time.time()
for i, p in enumerate(passwords):
    if stored_hash == hashlib.md5((salt + p).encode()).hexdigest():
        print('Hash match found, password: ' + p)
        end_md5 = time.time()
        print(f'Generated {i} md5 hashes in {end_md5-start_md5} seconds')
        break

start_pbkdf2 = time.time()

#Lets use 870000 iterations, which Django 5.0 uses, and try out creating hashes for 10 entries
iterations = 870000
for p in entries:
    hashlib.pbkdf2_hmac(
        "sha256",
        p.encode(),
        salt.encode(),
        iterations
    )

end_pbkdf2 = time.time()
print(f'Generated {len(entries)} PBDFK2 hashes in {end_pbkdf2-start_pbkdf2} seconds')