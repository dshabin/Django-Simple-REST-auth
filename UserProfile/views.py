# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer,UserProfileSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAdminUser
from .permissions import IsOwnerOrReadOnlyForUser
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework import permissions
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from .models import UserProfile
import requests
import random
from django.http import HttpResponse


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Enable filter,Enable search
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    # Fields for filter by
    filter_fields = ('is_staff','username')
    # Fields for search by
    search_fields = ('^username', )
    # Permission classes
    permission_classes = [IsOwnerOrReadOnlyForUser]
    # Ordering queryset by
    ordering_fields = ('username', 'email')
    # Default field for ordering
    ordering = ('username',)
    # Allowed Http methods excluded : DELETE , OPTIONS
    http_method_names = ['options','get', 'post','head']


    def list(self, request):
        queryset = User.objects.all()
        results = list()
        for user in queryset:
            if request.user == user :
                results.append(user)
        queryset = results
        serializer = UserSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        if not user == request.user:
            target = get_object_or_404(queryset,pk=0)
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)


    # Custom throtelling;change the user_post_protection in settings.py
    def get_throttles(self):
        if self.request.method not in permissions.SAFE_METHODS:
            self.throttle_scope = 'user_post_protection'
        return super(UsersViewSet, self).get_throttles()

    # Custom create method by username and password
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        # Check Fields validation, Except password
        serializer.is_valid(raise_exception=True)


        #Check validation of PASSWORD
        try:
            errors = dict()
            validators.validate_password(password=request.data.get('password'),user=request.data.get('username'))
        except ValidationError as e:
            errors['password'] = list(e.messages)
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)

        try:
            errors = dict()
            validate_email(request.data.get('email'))
        except ValidationError as e:
            errors['email'] = list(e.messages)
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)


        self.perform_create(serializer,request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    # Add password for User object
    def perform_create(self, serializer,request):
        serializer.save()
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username)
        self.create_user_profile(user,request)
        user.set_password(password)
        user.save()


    def create_user_profile(self,user_object,request):
        try:
            user_profile_object = UserProfile.objects.create(user=user_object)
            user_profile_object.username = user_object.username
            user_profile_object.save()
            user_object.username = request.data.get('email')
            user_object.save()
        except Exception as e:
            print(e)


    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['options','get','head']

    def list(self, request):
        queryset = UserProfile.objects.all()
        results = list()
        for user_profile in queryset:
            if request.user == user_profile.user :
                results.append(user_profile)
        queryset = results
        serializer = UserProfileSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = UserProfile.objects.all()
        user_profile = get_object_or_404(queryset, pk=pk)
        if not user_profile.user == request.user:
            target = get_object_or_404(queryset,pk=0)
        serializer = UserProfileSerializer(user_profile,context={'request': request})
        return Response(serializer.data)
