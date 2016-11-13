from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Establishment(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User)
    def __str__(self):
        return self.name

class Theatre(models.Model):
    establishment = models.ForeignKey(Establishment,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Employee(models.Model):
    Role_choices = (
        ('Manager', 'Manager'),
        ('Desk', 'Desk'),
        ('Help/Support', 'Help/Support'),
    )
    theatre = models.ForeignKey(Theatre,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    Role = models.CharField(max_length=50,choices=Role_choices)

    def __str__(self):
        return self.name + '-' + self.Role