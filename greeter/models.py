from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    expires_timestamp = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ()


class Greeting(models.Model):
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_day = models.IntegerField(blank=True, null=True)
    birth_month = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=50)
