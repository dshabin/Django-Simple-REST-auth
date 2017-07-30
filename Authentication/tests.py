# Create your tests here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
import json


# Test '/api-token-auth/'
class AuthenticationTestCase(APITestCase):

    '''
    Test GET request on '/authentication/'
    '''
    def test_get(self):
        url = '/authentication/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    '''
    Test POST request on '/authentication/' with bad username and password
    '''
    def test_post_bad_user(self):
        url = '/authentication/'
        data = {"username" : "someuser","password" : "somepassword"}
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,400)

    '''
    Test POST request on '/authentication/' with valid username and password
    '''
    def test_user_auth_success(self):
        username = "username"
        password = "password"
        user = User.objects.create(username=username)
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        url = '/authentication/'
        data = {"username" : "username","password" : "password"}
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,200)
