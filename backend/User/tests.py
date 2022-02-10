from distutils.log import Log
from urllib import response
from django.test import TestCase
import requests
import json

# Create your tests here.
class UserTestCase(TestCase):
    def test_user_login_REST(self):
        url = "http://127.0.0.1:8000/login/"
        data = {
            "username": "test-ppnk-api-2",
            "password": "iamtestpwd123"
        }

        response = requests.post(url, data=data)

        response_dict = json.loads(response.content.decode('utf-8'))
        login_key = response_dict['key']
        assert(login_key == "0ad71ca512601a5cbdecae046720bdd2341bf93e")

