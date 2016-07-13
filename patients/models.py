from __future__ import unicode_literals

import datetime
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    expires_timestamp = models.DateTimeField(blank=True, null=True)


class Greeting(models.Model):
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    dob = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=50)
