from __future__ import unicode_literals

from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=200)


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dob = models.DateTimeField
