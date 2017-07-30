# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework_jwt.views import ObtainJSONWebToken

#Add throttling on /api-token-auth/
class GetTokenApiWithLimit(ObtainJSONWebToken):
    def get_throttles(self):
        if self.request.method not in permissions.SAFE_METHODS:
            self.throttle_scope = 'obtain_jwt_token_protection'
        return super(GetTokenApiWithLimit, self).get_throttles()

ObtainJwtTokenProtectedView = GetTokenApiWithLimit.as_view()
