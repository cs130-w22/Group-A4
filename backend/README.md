# LazyTrip Backend API & Doc

## **Table of Content**
- [LazyTrip Backend API & Doc](#lazytrip-backend-api--doc)
  - [**Table of Content**](#table-of-content)
  - [**Project Setup**](#project-setup)
  - [**Run Project**](#run-project)
  - [**Login/Signup**](#loginsignup)
    - [1. Google OAuth Examples](#1-google-oauth-examples)
    - [2. Local Authentication System](#2-local-authentication-system)
  - [**Logout**](#logout)
  - [***CRUD* User Profile**](#crud-user-profile)
    - [1. As regular user](#1-as-regular-user)
    - [2. As admin (superuser)](#2-as-admin-superuser)
  - [TODO: ***CRUD* Itinerary**](#todo-crud-itinerary)


## **Project Setup**
```bash
# install pip file
pip install -r requirements.txt
# django setup
python manage.py makemigrations
python manage.py migrate
```

## **Run Project**
```bash
# run server listening on port 8000 by default
python manage.py runserver
```

## **Login/Signup**
Our backend support both local authentication and google authentication, here we will list short examples for each method.

### 1. Google OAuth Examples
The necessary configuration is already setup on [Google Developer Console](https://console.developers.google.com/apis/credentials/oauthclient/113665789634-ouu64vjjn7mnj0slrmtmm5e5gauu17o7.apps.googleusercontent.com?project=core-song-339901). We provide a url link for [google login window](https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id=113665789634-ouu64vjjn7mnj0slrmtmm5e5gauu17o7.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth%2Fgoogle%2Fcallback%2F&scope=profile&response_type=code&state=Uvpq2v78tkM&flowName=GeneralOAuthFlow), after confirming and choosing your google account at that window, it will redirect to `<front-end-url>` and reply to you with an `access_token`, that can be used in our backend token system. Simply adding this `access_token` to each of your request (JSON) for authentication.

### 2. Local Authentication System
We also provide registering and login using backend's authentication system. To register, you will need to send a `POST` request to http://127.0.0.1:8000/registration/, together with your username, password1, password2(for confirmation) and email. Like this:
```http
POST http://127.0.0.1:8000/registration/ HTTP/1.1
Content-Type: application/json

{
    "username": "testing-registration",
    "password1": "iamtestpwd123",
    "password2": "iamtestpwd123",
    "email": "test-api-registration@test.com"
}
```
If successful, backend will reply with `access_token`, `refresh_token` and basic `user` info, where the `access_token` can be used for authentication in future requests just like using Google Auth method above. To login, simply send a `POST` request to http://127.0.0.1:8000/login/, with your `username` and `password` added in the payload (JSON). Like this:
```http
POST http://127.0.0.1:8000/login/ HTTP/1.1
Content-Type: application/json

{
    "username": "testing-registration",
    "password": "iamtestpwd123"
}
```
If successful, it will return the same thing as when registration (`access_token`, `refresh_token` and `user`).

## **Logout**
Logout is used when you want to switch account, because the backend will set cookies and you *won't* be able to change account even if you provide a different `access_token`. You can send a `POST` request to http://127.0.0.1:8000/logout/ without adding anything. Once you are logged out, you need to ask for new `access_token` to log back in! Like this:
```http
POST http://127.0.0.1:8000/logout/ HTTP/1.1
```

## ***CRUD* User Profile**
### 1. As regular user
As a regular user, you can only view/update your own profile. To view your own information, send a `GET` request to http://127.0.0.1:8000/user/profile/ with your `access_token` added. Like this:
```http
GET http://127.0.0.1:8000/user/profile/ HTTP/1.1
Content-Type: application/json

{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ0NjQ3NDA2LCJpYXQiOjE2NDQ1NjEwMDYsImp0aSI6ImE4N2Q0ZjhmOGFiNDRmNzNhZDJkM2U4YzhlZGQ2NDc0IiwidXNlcl9pZCI6NH0._UfZD6JmlhY1Wkf-piz8Be727VTn6o50qtW2jRChuKA"
}
```
To update your own information, let's say you're user `id=4`, you can send a `PATCH` request to http://127.0.0.1:8000/user/update/4/. You can only update your own info, while admin is able to update every user's info. Like this: (Because `age` is inside `profile`, we wrap `age` with `profile`)
```http
PATCH http://127.0.0.1:8000/user/update/4/ HTTP/1.1
Content-Type: application/json

{
    "profile":{
        "age":"20"
    },
    "access_token": "<YOUR-OR-ADMIN-ACCESS-TOKEN>"
}
```
To delete your account, let's say you're user `id=4`, you can send a `DELETE` request to http://127.0.0.1:8000/user/delete/4/. You can only delete your own account, but if you are admin, you know what shit you can do. Like this:
```http
DELETE http://127.0.0.1:8000/user/delete/4/ HTTP/1.1
Content-Type: application/json

{
    "access_token": "<YOUR-OR-ADMIN-ACCESS-TOKEN>"
}
```

### 2. As admin (superuser)
As an admin, you can view information of each individual user (or together). To view all user info at once (might be large), Simply send a `GET` request to http://127.0.0.1:8000/user/ with your `access_token` added. Like this:
```http
GET http://127.0.0.1:8000/user/ HTTP/1.1
Content-Type: application/json

{
    "access_token": "<ADMIN'S ACCESS TOKEN>"
}
```
As an admin, you can also retrieve each individual user's information with their user ID (`id`). Let's say you want to view user with `id=4`, you can send a `GET` request to http://127.0.0.1:8000/user/profile/4/, with your `access_token` added. Like this:
```http
GET http://127.0.0.1:8000/user/profile/4/ HTTP/1.1
Content-Type: application/json

{
    "access_token": "<ADMIN'S ACCESS TOKEN>"
}
```

## TODO: ***CRUD* Itinerary**


<!-- ```
"""
Example: Login/Signup Using Google
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

``` -->