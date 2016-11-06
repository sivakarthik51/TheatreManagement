from __future__ import unicode_literals
import datetime
from django.db import models
from django.core.urlresolvers import reverse
from Establishments.models import Establishment,Theatre
# Create your models here.

class Movie(models.Model):
    theatre = models.ForeignKey(Theatre,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    meta_completed = models.BooleanField(default=False)
    movie_poster = models.FileField()


    def get_absolute_url(self):
        return reverse('Movies:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name + ' - ' + self.director

class Cast(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    person_name = models.CharField(max_length=255)
    character_name = models.CharField(max_length=100)

class Movie_Meta(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    runtime = models.CharField(max_length=100)
    release_date = models.CharField(max_length=20)

class Shows(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    show_time = models.DateTimeField(default=datetime.datetime.today())