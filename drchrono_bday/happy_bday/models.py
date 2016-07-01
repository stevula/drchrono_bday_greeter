from __future__ import unicode_literals

import datetime
from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return {name: self.name}


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dob = models.DateTimeField

    def __str__(self):
        return {name: self.name, dob: self.dob}

    def age(self):
        return datetime.year - self.dob.year
