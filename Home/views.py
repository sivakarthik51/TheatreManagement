from django.shortcuts import render
from django.views import generic
from Movies.models import Movie
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'Home/index.html'

    def get_queryset(self):
        return Movie.objects.all()