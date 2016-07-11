from __future__ import unicode_literals

import datetime
from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(models.Model):
    # many users can manage patients on behalf of one doctor
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s (DOB: %s)" % (self.name, self.dob)

    def age(self):
        # TODO: use dateutil lib
        return (datetime.datetime.now() - self.dob) / 365
