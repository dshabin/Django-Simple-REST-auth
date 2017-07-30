# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
import json
from django.core.urlresolvers import reverse



# Test '/users/'
class UsersTestCase(APITestCase):


    '''
    Test Create User with POST request
    '''
    def test_post_create_user(self):
        url = '/users/'
        data = {'username' : 'testuser','password' : 'password123'}
        response = self.client.post(url,data,format='multipart')
        self.assertEqual(response.status_code, 201)

    '''
    Test Create user with bad username and bad password
    '''
    def test_create_user_bad_username_bad_password(self):
        url = '/users/'
        bad_username = '!@$#$!@@!%'
        bad_password = '1'
        data = {'username' : bad_username,'password' : bad_password}
        response = self.client.post(url,data,format='multipart')
        self.assertEqual(response.status_code,400)

    '''
    Test Create user without password
    '''
    def test_create_user_without_password(self):
        url = '/users/'
        data = {'username' : 'testuser'}
        response = self.client.post(url,data,format='multipart')
        self.assertEqual(response.status_code, 400)

    '''
    Test Delete user
    '''
    def test_delete_user(self):
        username = "username"
        password = "password"
        user = User.objects.create(username=username)
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        url = '/authentication/'
        data = {"username" : "username","password" : "password"}
        response = self.client.post(url,data,format='json')
        token = response.data['token']
        user_url = reverse('user-detail', kwargs={'pk': user.id})
        response = self.client.delete(user_url,{},HTTP_AUTHORIZATION='JWT ' + token,format='json')
        self.assertEqual(response.status_code,405)

    '''
    Test Update user , PUT method

    def test_update_user(self):
        username = "username"
        password = "password"
        user = User.objects.create(username=username)
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        url = '/authentication/'
        data = {"username" : "username","password" : "password"}
        response = self.client.post(url,data,format='json')
        token = response.data['token']
        user_url = reverse('user-detail', kwargs={'pk': user.id})
        new_data = {"username" : "new_username","password" : "new_password"}
        response = self.client.put(user_url,new_data,HTTP_AUTHORIZATION='JWT ' + token,format='json')
        self.assertEqual(response.data['username'],new_data['username'])



    Test Update user (partial-update) , PATCH method

    def test_update_user(self):
        username = "username"
        password = "password"
        user = User.objects.create(username=username)
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        url = '/authentication/'
        data = {"username" : "username","password" : "password"}
        response = self.client.post(url,data,format='json')
        token = response.data['token']
        user_url = reverse('user-detail', kwargs={'pk': user.id})
        new_data = {"username" : "new_username"}
        response = self.client.patch(user_url,new_data,HTTP_AUTHORIZATION='JWT ' + token,format='json')
        self.assertEqual(response.data['username'],new_data['username'])

    '''
