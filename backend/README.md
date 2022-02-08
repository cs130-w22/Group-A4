# LazyTrip Backend
[![Github CI](https://github.com/cs130-w22/Group-A4/actions/workflows/django-ci.yml/badge.svg)](https://github.com/cs130-w22/Group-A4/actions/workflows/django-ci.yml)

## Project setup
```
pip install -r requirements.txt
```

## Run Project
```
# django setup
python manage.py makemigrations
python manage.py migrate
# run server listening on port 8000 by default
python manage.py runserver
```

## REST API: Login using Google OAuth Examples
```
"""
Example: Login Using Google
1. Send GET request to our app's Google login API endpoint
"""
curl -I http://localhost:8000/auth/google/url/

"""
2. It will return HTTP response "302 Found" with one of the header field: "Location: <some-google-url>"
3. Open browser and connects to that <some-google-url>, it will popup google login prompt
4. After login using your account, it will redirects to "<FRONTEND_URL>/auth/google?<params>". Here, <FRONTEND_URL> is set to "http://localhost:8000" for backend testing, normally should set to front-end url in the future. Here <params> contain info about the logged in user, we need the "code" part from it, let's say "code=4%2F0AX4XfWjhj0rsggsdUZ7nt_LHvqpb7VIurYiEdXyANjrui2XPbk6eBlxPPEhPYbSOproUdw"
5. Use the code to get back a Token key from backend
"""
curl localhost:8000/auth/google/ -d code=4%2F0AX4XfWjhj0rsggsdUZ7nt_LHvqpb7VIurYiEdXyANjrui2XPbk6eBlxPPEhPYbSOproUdw

"""
6. If successful, backend will return a json format of Token key, let's say {"key":"c7707485ecfe8c39a89ea0389b34ef4ee9b1e7b2"}, we then can use this token key to access things that requires authorization. Let's say we want to access all user info (of course only superuser can do that, can be set in django admin page)
"""
curl localhost:8000/user/ -H "Authorization: Token c7707485ecfe8c39a89ea0389b34ef4ee9b1e7b2"

```