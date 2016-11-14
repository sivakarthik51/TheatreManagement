from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserWallet(models.Model):
    user = models.OneToOneField(User)
    credit = models.FloatField(default=1000.0)

    def __str__(self):
        return self.user.first_name +'\'s profile'