from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
