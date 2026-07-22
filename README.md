# Project

A project assignment for the course Cyber Security Base 2025. A web application with security flaws and the fixes to correct the flaws.

## Running the application
After cloning the repository, navigate to the folder where manage.py is, then boot the server
``` 
python manage.py runserver
```
After implementing the fixes you probably need to install the logging tool used in the project
```
pip install django-axes
```
## Implementing the fixes
De-comment everything in the file [settings](https://github.com/ogvirtan/csmooc-project1/blob/master/mysite/mysite/settings.py), except for the last comment. Remove the last comment and everything under it to get rid of the application using md5 for password hashing.
Everywhere else the commented out code sections should be de-commented, and the now de-commented parts should replace existing functionalities with the same names.

## Testing weaknesses
In the vuln directory there are some tools to test weaknesses

### Injection
Injection.txt contains some inputs you can paste into the search field found on the user page.

### Credential stuffer
With the application running, run the stuffer and provide it with a username. The stuffer will attempt to log in to that users account by trying entries in a small array of weak passwords. After implementing the fixes you will be timed out if running the credential stuffer, here's how to reset the logger
```
python manage.py axes_reset
```

### CSRF-attempts
From the vuln directory you can run a server with 
``` 
python -m http.server 9000
``` 
select the html to open based on whether you are running the fixed version or not. For the fixed version try out csrf-attempt-on-post.html and for the vulnerable version try out csrf-attempt-on-get.html. The application needs to be running while doing this. Make sure both the application and the server run from vuln use 127.0.0.1 or localhost. If one has localhost and one has 127.0.0.1 it won't work.

### Password hash matching
Run password_hash_matching.py to see the difference in speeds of generating md5 and pbkdf2 hashes.
