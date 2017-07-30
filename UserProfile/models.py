# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=50,default="0")
    firstname_lastname = models.CharField(max_length=50,default="0")
    telephone = models.CharField(max_length=20,default="0")
    email_address = models.CharField(max_length=50,default = "0")
    id_card_img_address = models.CharField(max_length=100,default="0")
    verify_id = models.CharField(max_length=20,default="0")
    is_email_verified = models.BooleanField(default=False)
    is_identity_verified = models.BooleanField(default=False)
    is_home_telephone_verified = models.BooleanField(default=False)
    home_telephone = models.CharField(max_length=20,default="0")
    address = models.CharField(max_length=100,default = "0")
    card_number = models.CharField(max_length=20,default = "0")


    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
