from __future__ import unicode_literals

import datetime
from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.dob)

    def age(self):
        # TODO: use dateutil lib
        return (datetime.datetime.now() - self.dob) / 365
