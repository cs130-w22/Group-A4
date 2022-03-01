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
  - [**User Profile** Read/Update/Delete](#user-profile-readupdatedelete)
    - [1. As regular user](#1-as-regular-user)
    - [2. As admin (superuser)](#2-as-admin-superuser)
  - [**Itinerary** CRUD](#itinerary-crud)
    - [Create An Itinerary After Logged In](#create-an-itinerary-after-logged-in)
    - [Retrieve All Itineraries Created by the Logged-in User [SIMPLIFIED VERSION]](#retrieve-all-itineraries-created-by-the-logged-in-user-simplified-version)
    - [Retrieve All Itineraries Created by the Logged-in User [DETAILED VERSION]](#retrieve-all-itineraries-created-by-the-logged-in-user-detailed-version)
    - [Retrieve Itinerary by ID [DETAILED VERSION]](#retrieve-itinerary-by-id-detailed-version)
    - [Update Itinerary by the ID](#update-itinerary-by-the-id)
  - [**TripEvent** CRUD](#tripevent-crud)
    - [Create an TripEvent Under an Itinerary](#create-an-tripevent-under-an-itinerary)
    - [Retrieve an TripEvent by the ID](#retrieve-an-tripevent-by-the-id)
    - [Update an TripEvent by the ID](#update-an-tripevent-by-the-id)
  - [**Query Place Info**](#query-place-info)
      - [Getting Place Recommendations Using Name of the Destination:](#getting-place-recommendations-using-name-of-the-destination)
      - [Getting Details of Exact Attraction (`place_id`):](#getting-details-of-exact-attraction-place_id)
  - [**Scheduling API**](#scheduling-api)


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
The necessary configuration is already setup on [Google Developer Console](https://console.developers.google.com/apis/credentials/oauthclient/113665789634-ouu64vjjn7mnj0slrmtmm5e5gauu17o7.apps.googleusercontent.com?project=core-song-339901). We provide a url link for [google login window](https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id=113665789634-ouu64vjjn7mnj0slrmtmm5e5gauu17o7.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth%2Fgoogle%2Fcallback%2F&scope=profile&response_type=code&state=Uvpq2v78tkM&flowName=GeneralOAuthFlow), after confirming and choosing your google account at that window, it will redirect to `<front-end-url>` and reply to you with an `access_token`, that can be request a JWT Token from our backend token system. Simply adding this `access_token` got from google your login `POST` request, response will come with an `access_token` that can be used with our backend.
```http
POST http://127.0.0.1:8000/auth/google/ HTTP/1.1
Content-Type: application/json

{
    "access_token": "<ACCESS-TOKEN-YOU-GET-FROM-GOOGLE>"
}
```

<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Thu, 24 Feb 2022 01:29:18 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Cookie, Origin
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 605
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
Set-Cookie: LazyTrip-auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1NzUyNTU4LCJpYXQiOjE2NDU2NjYxNTgsImp0aSI6IjE0NjJlNTQyZDY1YTRmNzg5NmM2NzU5MWEzYzAyZWYyIiwidXNlcl9pZCI6MX0.ETHaOxtIa94OBN_HHXd6oSaxwgb0SFElU_AViRZx3ec; expires=Fri, 25 Feb 2022 01:29:18 GMT; HttpOnly; Max-Age=86400; Path=/; SameSite=Lax,LazyTrip-refresh-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NjI3MDk1OCwiaWF0IjoxNjQ1NjY2MTU4LCJqdGkiOiIxNjVkYWRmNjljZjE0N2FjYjU2NTA0MTA3ODcxZWQyZCIsInVzZXJfaWQiOjF9.pvybM7dfkdNlCQrTqMnA6IiAZhDb1u6c5HR5C1Q7JJk; expires=Thu, 03 Mar 2022 01:29:18 GMT; HttpOnly; Max-Age=604800; Path=/; SameSite=Lax,csrftoken=gHFeK8GgtanhnoQ1ycSD83zfJFsz9uGw4oxBaZ1XgRFjlQFj1e2hP1grii6VR84T; expires=Thu, 23 Feb 2023 01:29:18 GMT; Max-Age=31449600; Path=/; SameSite=Lax,sessionid=j070bseea1yizkox9hk0eauepxgptivz; expires=Thu, 10 Mar 2022 01:29:18 GMT; HttpOnly; Max-Age=1209600; Path=/; SameSite=Lax

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1NzUyNTU4LCJpYXQiOjE2NDU2NjYxNTgsImp0aSI6IjE0NjJlNTQyZDY1YTRmNzg5NmM2NzU5MWEzYzAyZWYyIiwidXNlcl9pZCI6MX0.ETHaOxtIa94OBN_HHXd6oSaxwgb0SFElU_AViRZx3ec",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NjI3MDk1OCwiaWF0IjoxNjQ1NjY2MTU4LCJqdGkiOiIxNjVkYWRmNjljZjE0N2FjYjU2NTA0MTA3ODcxZWQyZCIsInVzZXJfaWQiOjF9.pvybM7dfkdNlCQrTqMnA6IiAZhDb1u6c5HR5C1Q7JJk",
  "user": {
    "pk": 1,
    "username": "admin",
    "email": "admin@nimda.com",
    "first_name": "admin's first name",
    "last_name": ""
  }
}
```

</details>
<br></br>

Once you got the `access_token` (from our backend, not Google), you can add that as an header in each of your request representing the user identity. Like this:
```http
POST http://127.0.0.1:8000/any/api/request/that/needs/authentication/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-ACCESS-TOKEN>

{
    "field1": "something you are posting",
    "field2": "other things..."
}
```

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
Logout is used when you want to switch account, the response will contain an '*empty*' `set-cookie` header which clears your brower's cookie for the token if front-end handles that `set-cookie` header. You can send a `POST` request to http://127.0.0.1:8000/logout/ without adding anything. Like this:
```http
POST http://127.0.0.1:8000/logout/ HTTP/1.1
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Thu, 24 Feb 2022 01:31:57 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin, Cookie
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 37
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
Set-Cookie: LazyTrip-auth=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/,LazyTrip-refresh-token=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/,sessionid=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/; SameSite=Lax

{
  "detail": "Successfully logged out."
}
```

</details>
<br></br>


## **User Profile** Read/Update/Delete
### 1. As regular user
As a regular user, you can only view/update your own profile. To view your own information, send a `GET` request to http://127.0.0.1:8000/user/profile/ with your `access_token` added. Like this:
```http
GET http://127.0.0.1:8000/user/profile/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-ACCESS-TOKEN>
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Thu, 24 Feb 2022 01:34:16 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin
Allow: GET, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 1228
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{
  "id": 1,
  "username": "admin",
  "first_name": "admin's first name",
  "last_name": "",
  "email": "admin@nimda.com",
  "date_joined": "2022-01-31T02:07:51.283530Z",
  "last_login": "2022-02-24T01:34:13.123777Z",
  "profile": {
    "age": 12,
    "bio": "",
    "location": ""
  },
  "itinerary": [
    {
      "id": 1,
      "title": "My First Itinerary!!!",
      "desc": "Edit this to be the description of your travel plan!",
      "created_at": "2022-02-24T00:08:42.950862Z",
      "last_modified": "2022-02-24T00:58:59.473301Z",
      "user": 1,
      "trip_event": [
        {
          "id": 1,
          "place_id": "<place_id-PLACEHOLDER>",
          "start_time": "2022-02-23T14:30:00Z",
          "end_time": "2022-02-23T17:30:00Z",
          "itin": 1,
          "place_json": "<place_json-PLACEHOLDER>"
        },
        {
          "id": 2,
          "place_id": "<place_id-PLACEHOLDER>",
          "start_time": "2022-02-23T14:30:00Z",
          "end_time": "2022-02-23T17:30:00Z",
          "itin": 1,
          "place_json": "<place_json-PLACEHOLDER-2>"
        }
      ]
    },
    {
      "id": 2,
      "title": "My Second Itinerary!!!",
      "desc": "Edit this to be the description of your travel plan!",
      "created_at": "2022-02-24T00:58:45.244661Z",
      "last_modified": "2022-02-24T00:59:42.399455Z",
      "user": 1,
      "trip_event": []
    },
    {
      "id": 3,
      "title": "My's Third Itinerary!",
      "desc": "Edit this to be the description of your travel plan!",
      "created_at": "2022-02-24T00:58:51.610574Z",
      "last_modified": "2022-02-24T00:58:51.610622Z",
      "user": 1,
      "trip_event": []
    }
  ]
}

```

</details>
<br></br>

To update your own information, let's say you're user `id=4`, you can send a `PATCH` request to http://127.0.0.1:8000/user/profile/4/. You can only update your own info, while admin is able to update every user's info. Like this: (Because `age` is inside `profile`, we wrap `age` with `profile`)
```http
PATCH http://127.0.0.1:8000/user/profile/4/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-ACCESS-TOKEN>

{
    "profile":{
        "age":"20"
    }
}
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Thu, 24 Feb 2022 01:36:05 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin
Allow: GET, PUT, PATCH, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 270
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{
  "id": 4,
  "username": "test-ppnk1",
  "first_name": "test_firstname",
  "last_name": "test_lastname",
  "email": "",
  "date_joined": "2022-01-31T02:11:34.292524Z",
  "last_login": "2022-02-24T01:33:37.391987Z",
  "profile": {
    "age": 20,
    "bio": "I'm PPNK",
    "location": "Los Angeles, CA"
  },
  "itinerary": []
}

```

</details>
<br></br>

To delete your account, let's say you're user `id=4`, you can send a `DELETE` request to http://127.0.0.1:8000/user/delete/4/. You can only delete your own account, but if you are admin, you know what shit you can do. Like this:
```http
DELETE http://127.0.0.1:8000/user/delete/4/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>
```

### 2. As admin (superuser)
As an admin, you can view information of each individual user (or together). To view all user info at once (might be large), Simply send a `GET` request to http://127.0.0.1:8000/user/ with your `access_token` added. Like this:
```http
GET http://127.0.0.1:8000/user/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Thu, 24 Feb 2022 01:37:22 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin
Allow: GET, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 3635
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

[
  {
    "id": 1,
    "username": "admin",
    "first_name": "admin's first name",
    "last_name": "",
    "email": "admin@nimda.com",
    "date_joined": "2022-01-31T02:07:51.283530Z",
    "last_login": "2022-02-24T01:34:13.123777Z",
    "profile": {
      "age": 12,
      "bio": "",
      "location": ""
    },
    "itinerary": [
      {
        "id": 1,
        "title": "My First Itinerary!!!",
        "desc": "Edit this to be the description of your travel plan!",
        "created_at": "2022-02-24T00:08:42.950862Z",
        "last_modified": "2022-02-24T00:58:59.473301Z",
        "user": 1,
        "trip_event": [
          {
            "id": 1,
            "place_id": "<place_id-PLACEHOLDER>",
            "start_time": "2022-02-23T14:30:00Z",
            "end_time": "2022-02-23T17:30:00Z",
            "itin": 1,
            "place_json": "<place_json-PLACEHOLDER>"
          },
          {
            "id": 2,
            "place_id": "<place_id-PLACEHOLDER>",
            "start_time": "2022-02-23T14:30:00Z",
            "end_time": "2022-02-23T17:30:00Z",
            "itin": 1,
            "place_json": "<place_json-PLACEHOLDER-2>"
          }
        ]
      },
      {
        "id": 2,
        "title": "My Second Itinerary!!!",
        "desc": "Edit this to be the description of your travel plan!",
        "created_at": "2022-02-24T00:58:45.244661Z",
        "last_modified": "2022-02-24T00:59:42.399455Z",
        "user": 1,
        "trip_event": []
      },
      {
        "id": 3,
        "title": "My's Third Itinerary!",
        "desc": "Edit this to be the description of your travel plan!",
        "created_at": "2022-02-24T00:58:51.610574Z",
        "last_modified": "2022-02-24T00:58:51.610622Z",
        "user": 1,
        "trip_event": []
      }
    ]
  },
  {
    "id": 2,
    "username": "test-ppnk1",
    "first_name": "test_firstname",
    "last_name": "test_lastname",
    "email": "",
    "date_joined": "2022-01-31T02:11:34.292524Z",
    "last_login": "2022-02-24T01:33:37.391987Z",
    "profile": {
      "age": 23,
      "bio": "I'm PPNK",
      "location": "Los Angeles, CA"
    },
    "itinerary": []
  },
  {
    "id": 3,
    "username": "test-ppnk-api",
    "first_name": "",
    "last_name": "",
    "email": "test-api-registration@test.com",
    "date_joined": "2022-01-31T09:54:16.142804Z",
    "last_login": null,
    "profile": {
      "age": 0,
      "bio": "Edit this to be your bio.",
      "location": ""
    },
    "itinerary": []
  },
  {
    "id": 4,
    "username": "test-ppnk-api-2",
    "first_name": "",
    "last_name": "",
    "email": "test-api-registration-2@test.com",
    "date_joined": "2022-01-31T09:58:08.859386Z",
    "last_login": "2022-02-23T23:20:36.502192Z",
    "profile": {
      "age": 0,
      "bio": "Edit this to be your bio.",
      "location": ""
    },
    "itinerary": []
  },
  {
    "id": 5,
    "username": "test-ppnk-api-3",
    "first_name": "",
    "last_name": "",
    "email": "test-api-registration-3@test.com",
    "date_joined": "2022-01-31T10:11:53.796783Z",
    "last_login": "2022-01-31T10:12:26.780984Z",
    "profile": {
      "age": 0,
      "bio": "Edit this to be your bio.",
      "location": ""
    },
    "itinerary": []
  },
  {
    "id": 6,
    "username": "zongnan",
    "first_name": "Zongnan",
    "last_name": "Bao",
    "email": "zb3@g.ucla.edu",
    "date_joined": "2022-02-08T22:18:50Z",
    "last_login": "2022-02-17T20:34:50.461959Z",
    "profile": {
      "age": 0,
      "bio": "Edit this to be your bio.",
      "location": ""
    },
    "itinerary": []
  },
  {
    "id": 7,
    "username": "zongnan3",
    "first_name": "Zongnan",
    "last_name": "Bao",
    "email": "zb3@illinois.edu",
    "date_joined": "2022-02-08T23:32:32Z",
    "last_login": "2022-02-10T01:28:03Z",
    "profile": {
      "age": 0,
      "bio": "Edit this to be your bio.",
      "location": ""
    },
    "itinerary": []
  },
  {
    "id": 8,
    "username": "zongnan8",
    "first_name": "Zongnan",
    "last_name": "Bao",
    "email": "zongnan.bao@gmail.com",
    "date_joined": "2022-02-08T23:32:50Z",
    "last_login": "2022-02-10T01:27:41Z",
    "profile": {
      "age": 0,
      "bio": "Edit this to be your bio.",
      "location": ""
    },
    "itinerary": []
  },
  {
    "id": 9,
    "username": "zongnan60",
    "first_name": "Zongnan",
    "last_name": "Bao",
    "email": "nick19981122@gmail.com",
    "date_joined": "2022-02-10T01:32:23.933580Z",
    "last_login": "2022-02-10T01:32:23.962981Z",
    "profile": {
      "age": 0,
      "bio": "Edit this to be your bio.",
      "location": ""
    },
    "itinerary": []
  },
  {
    "id": 10,
    "username": "dyyfk",
    "first_name": "dyyfk",
    "last_name": "dyyfk",
    "email": "879608095@qq.com",
    "date_joined": "2022-02-10T02:19:06.766937Z",
    "last_login": "2022-02-10T02:49:18.634829Z",
    "profile": {
      "age": 0,
      "bio": "Edit this to be your bio.",
      "location": ""
    },
    "itinerary": []
  }
]

```

</details>
<br></br>

As an admin, you can also retrieve each individual user's information with their user ID (`id`). Let's say you want to view user with `id=4`, you can send a `GET` request to http://127.0.0.1:8000/user/profile/4/, with your `access_token` added. Like this:
```http
GET http://127.0.0.1:8000/user/profile/4/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>
```

## **Itinerary** CRUD
### Create An Itinerary After Logged In
To create a new itinerary asscociated with logged-in user, send `POST` to http://127.0.0.1:8000/trip/itinerary/create/ with your `access_token` added. Like this:
```http
POST http://127.0.0.1:8000/trip/itinerary/create/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>

{
    "title": "My First Itinerary!"
}
```

### Retrieve All Itineraries Created by the Logged-in User [SIMPLIFIED VERSION]
As a regular user, you can retrieve all Itineraries created by you, they would be presented in simplified format (only `id`, `title`, `last_modified` is returned, you can use `id` to query a more detailed information). Send `GET` to http://127.0.0.1:8000/trip/itinerary/ with your token added. Like this:
```http
GET http://127.0.0.1:8000/trip/itinerary/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Thu, 24 Feb 2022 01:38:18 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin
Allow: GET, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 271
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

[
  {
    "id": 1,
    "title": "My First Itinerary!!!",
    "last_modified": "2022-02-24T00:58:59.473Z"
  },
  {
    "id": 2,
    "title": "My Second Itinerary!!!",
    "last_modified": "2022-02-24T00:59:42.399Z"
  },
  {
    "id": 3,
    "title": "My's Third Itinerary!",
    "last_modified": "2022-02-24T00:58:51.610Z"
  }
]
```

</details>
<br></br>

### Retrieve All Itineraries Created by the Logged-in User [DETAILED VERSION]
As an user, you can also retrieve all itineraries along with every bit of detail by sending `GET` to http://127.0.0.1:8000/trip/itinerary/all/. Like this:
```http
GET http://127.0.0.1:8000/trip/itinerary/all/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Thu, 24 Feb 2022 01:40:44 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin
Allow: GET, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 982
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

[
  {
    "id": 1,
    "title": "My First Itinerary!!!",
    "desc": "Edit this to be the description of your travel plan!",
    "created_at": "2022-02-24T00:08:42.950862Z",
    "last_modified": "2022-02-24T00:58:59.473301Z",
    "user": 1,
    "trip_event": [
      {
        "id": 1,
        "place_id": "<place_id-PLACEHOLDER>",
        "start_time": "2022-02-23T14:30:00Z",
        "end_time": "2022-02-23T17:30:00Z",
        "itin": 1,
        "place_json": "<place_json-PLACEHOLDER>"
      },
      {
        "id": 2,
        "place_id": "<place_id-PLACEHOLDER>",
        "start_time": "2022-02-23T14:30:00Z",
        "end_time": "2022-02-23T17:30:00Z",
        "itin": 1,
        "place_json": "<place_json-PLACEHOLDER-2>"
      }
    ]
  },
  {
    "id": 2,
    "title": "My Second Itinerary!!!",
    "desc": "Edit this to be the description of your travel plan!",
    "created_at": "2022-02-24T00:58:45.244661Z",
    "last_modified": "2022-02-24T00:59:42.399455Z",
    "user": 1,
    "trip_event": []
  },
  {
    "id": 3,
    "title": "My's Third Itinerary!",
    "desc": "Edit this to be the description of your travel plan!",
    "created_at": "2022-02-24T00:58:51.610574Z",
    "last_modified": "2022-02-24T00:58:51.610622Z",
    "user": 1,
    "trip_event": []
  }
]

```

</details>
<br></br>

### Retrieve Itinerary by ID [DETAILED VERSION]
To retrieve itinerary by id, you can send a `GET` request to http://127.0.0.1:8000/trip/itinerary/#(id)/, tripevents within this itinerary are grouped by date. Request like this:
```http
GET http://127.0.0.1:8000/trip/itinerary/2/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Tue, 01 Mar 2022 09:15:45 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin
Allow: GET, PUT, PATCH, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 1352
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{
  "id": 31,
  "title": "Your Auto Scheduled Trip",
  "desc": "Edit this to be the description of your travel plan!",
  "created_at": "2022-02-25T02:04:06.593162Z",
  "last_modified": "2022-02-25T02:04:06.593162Z",
  "user": 1,
  "trip_event": {
    "2022-02-22": [
      {
        "id": 161,
        "place_id": "ChIJh30fAVnGwoAR5gZouxCUABw",
        "place_name": "Studio For Southern California",
        "start_time": "2022-02-22T08:30:00Z",
        "end_time": "2022-02-22T11:00:00Z",
        "itin": 31,
        "place_json": ""
      },
      {
        "id": 162,
        "place_id": "ChIJ-1Vb4UTGwoARANaWGbqWTUA",
        "place_name": "Avila Adobe",
        "start_time": "2022-02-22T11:30:00Z",
        "end_time": "2022-02-22T14:00:00Z",
        "itin": 31,
        "place_json": ""
      },
      {
        "id": 163,
        "place_id": "ChIJSTW1vEXGwoARuir3gc9Q2SA",
        "place_name": "Chinese American Museum",
        "start_time": "2022-02-22T14:30:00Z",
        "end_time": "2022-02-22T17:00:00Z",
        "itin": 31,
        "place_json": ""
      },
      {
        "id": 164,
        "place_id": "ChIJj2tUC2bGwoARwqdCDE37YD0",
        "place_name": "San Antonio Winery",
        "start_time": "2022-02-22T17:30:00Z",
        "end_time": "2022-02-22T20:00:00Z",
        "itin": 31,
        "place_json": ""
      }
    ],
    "2022-02-23": [
      {
        "id": 165,
        "place_id": "ChIJP5P8tcrHwoAR5VP3q2oOrzU",
        "place_name": "Hive Gallery & Studios",
        "start_time": "2022-02-23T08:30:00Z",
        "end_time": "2022-02-23T11:00:00Z",
        "itin": 31,
        "place_json": ""
      },
      {
        "id": 166,
        "place_id": "ChIJbQ_1ObbHwoARlVhDqpRy3Gs",
        "place_name": "Grand Hope Park",
        "start_time": "2022-02-23T11:30:00Z",
        "end_time": "2022-02-23T14:00:00Z",
        "itin": 31,
        "place_json": ""
      }
    ]
  }
}

```

</details>
<br></br>


### Update Itinerary by the ID
To update an itinerary, you need the `id` of this itinerary, simply send `PATCH` to http://127.0.0.1:8000/trip/itinerary/#(id)/, with token added. As usual, user will have permission to update itinerary belongs to them, while admin can edit any itinerary given an `id`. Like this:
```http
PATCH http://127.0.0.1:8000/trip/itinerary/2/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>

{
    "title": "Updated Itinerary Title"
}
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 200 OK
Date: Thu, 24 Feb 2022 01:46:23 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin
Allow: GET, PUT, PATCH, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 218
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{
  "id": 2,
  "title": "Updated Itinerary Title",
  "desc": "Edit this to be the description of your travel plan!",
  "created_at": "2022-02-24T00:58:45.244661Z",
  "last_modified": "2022-02-24T01:46:23.369164Z",
  "user": 1,
  "trip_event": []
}

```

</details>
<br></br>

## **TripEvent** CRUD
<!-- `NOTE:` Since `TripEvent` does not have owner (user) field, you can only identify which user owns this `TripEvent` by looking at the ownership of this `TripEvent`'s `Itinerary`, `Itinerary` will have a field named `user` to identify which user this `Itinerary` belongs to.  -->

### Create an TripEvent Under an Itinerary
To create an TripEvent, you need to first know which Itinerary it belongs to, let's say you want to create a TripEvent that go to UCLA during `14:30` to `17:30`, under the Itinerary titled `"Updated Itinerary Title"` (`id=2`). You can send a `POST` request to http://127.0.0.1:8000/trip/event/create/. It will be succefully created only if you are the owner of Itinerary (`id=2`) or you are the holy-moly admin. Like this:
```http
POST http://127.0.0.1:8000/trip/event/create/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>

{
    "place_id": "<UCLA-place_id-PLACEHOLDER>",
    "itin": "2",
    "start_time": "2022-02-22 14:30",
    "end_time": "2022-02-22 17:30"
}
```
<details>
<summary> Response Example</summary>

```http
HTTP/1.1 201 Created
Date: Thu, 24 Feb 2022 01:49:14 GMT
Server: WSGIServer/0.2 CPython/3.10.2
Content-Type: application/json
Vary: Accept, Origin
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 168
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{
  "id": 3,
  "place_id": "<UCLA-place_id-PLACEHOLDER>",
  "start_time": "2022-02-22T14:30:00Z",
  "end_time": "2022-02-22T17:30:00Z",
  "itin": 2,
  "place_json": "<place_json-PLACEHOLDER>"
}
```

</details>
<br></br>

### Retrieve an TripEvent by the ID
As a regular user, you probably don't need to retrieve single TripEvent by the ID, you can instead retrieve your Itineraries which will contain every TripEvent inside them. **But** as an admin, it's reasonable to do so. Just send `GET` request to http://127.0.0.1:8000/trip/event/10/ if you want to view specific TripEvent with `id=10`. Like this:
```http
GET http://127.0.0.1:8000/trip/event/10/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>
```


### Update an TripEvent by the ID
It's simple to update an TripEvent, let's say you want to update your UCLA trip to a USC trip and move to `1 hour` later, you'll need to know the `id` of the TripEvent (like `id=10`), and send a `PATCH` request to http://127.0.0.1:8000/trip/event/10/. Like this:
```http
PATCH http://127.0.0.1:8000/trip/event/10/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>

{
    "place_id": "<USC-place_id-PLACEHOLDER>",
    "start_time": "2022-02-22 15:30",
    "end_time": "2022-02-22 18:30"
}
```
You can also move this TripEvent under other Itinerary, but you can only move to those Itinerary that belongs to you (or you are admin). Like this:
```http
PATCH http://127.0.0.1:8000/trip/event/10/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>

{
    "itin": "20", # assume itin 20 belongs to you
}
```


## **Query Place Info**
#### Getting Place Recommendations Using Name of the Destination:
We use `URL parameters` as query method, you need to specify the name of the location (don't have to be exact, such as "`Westwood`"). It will be matched to the most similar places, and using that as the query location to return back to you suggested attractions. Like this:
```http
GET http://127.0.0.1:8000/trip/search/loc?location=Westwood HTTP/1.1
```

#### Getting Details of Exact Attraction (`place_id`):
Instead of getting suggestions around a place, you can also get the information of an exact attraction based on the `place_id` (the unique object ID of GoogleMap API for each place). It has MUCH MUCH MORE detailed information about that exact attraction. We use `URL parameters` as query method, simply send a `GET` request to http://127.0.0.1:8000/trip/search/place-id, with parameter `id=<place_id>`
```http
GET http://127.0.0.1:8000/trip/search/place_id?id=ChIJD0eFf57DwoAR2VMsk3eVhn8 HTTP/1.1
```

## **Scheduling API**
To request a itinerary schedule, you need to prepare some data entered by user, and send a POST request to http://127.0.0.1:8000/trip/schedule/:
```http
POST http://127.0.0.1:8000/trip/schedule/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <YOUR-OR-ADMIN-ACCESS-TOKEN>

{
    "places": [
        {}, {}, {}, ...
    ],
    "wakeUpTime": "%HH:%MM",
    "dates": ["%YYYY-%MM-%DD", "%YYYY-%MM-%DD", "%YYYY-%MM-%DD"],
    "hotel": {} // optional
}
```
The response will be the newly generated `id`, you can use that to query the detail of that specific itinerary.

<!-- ### Getting Attraction Suggestions Based on Location Chosen (Deprecated, but still usable :))
Once user chooses a place, you can send the coordinate or the name of the place to backend, the backend will retrieve relevant attractions and get back to you. That said, there are 2 ways to give backend users' places of interests, both using `GET` request to http://127.0.0.1:8000/trip/search/loc/.
#### 1. Using exact coordinate:
Specify the longitude and latitude in the JSON data, both are `string` input (they will be converted to `float` in the backend), like this:
```http
GET http://127.0.0.1:8000/trip/search/loc/ HTTP/1.1
Content-Type: application/json

{
    "lon": "-118.4085",
    "lat": "33.9416",
    "access_token": "<YOUR-ACCESS-TOKEN>"
}
```
#### 2. Using name of the location: (Deprecated, but still usable :))
Specify the name of the location (don't have to be exact, but a bit more detail is good, such as using "`Westwood, Los Angeles`" instead of "`Westwood`", because there are westwoods in New York). It will be matched to the most similar places, and using that as the query location to return back to you suggested attractions. Like this:
```http
GET http://127.0.0.1:8000/trip/search/loc/ HTTP/1.1
Content-Type: application/json

{
    "location": "Westwood, Los Angeles",
    "access_token": "<YOUR-ACCESS-TOKEN>"
}
``` -->

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
