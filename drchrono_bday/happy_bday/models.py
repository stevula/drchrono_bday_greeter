from __future__ import unicode_literals

from django.db import models


class Doctor(models.model):
    name = models.CharField(max_length=200)


class Patient(models.Model):
    doctor = models.ForeignKey(QUestion, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dob = models.DateTimeField
