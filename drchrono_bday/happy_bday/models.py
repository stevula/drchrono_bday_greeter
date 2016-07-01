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
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.dob)

    def age(self):
        return datetime.datetime.now().year - self.dob
