from __future__ import unicode_literals
import datetime
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

class Movie(models.Model):
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