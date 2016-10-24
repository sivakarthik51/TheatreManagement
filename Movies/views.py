from django.shortcuts import render
from .models import Movie,Cast
# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

class IndexView(generic.ListView):
    template_name = 'Movies/index.html'
    context_object_name = 'all_Movies'

    def get_queryset(self):
        return Movie.objects.all()

class DetailView(generic.DetailView):
    model = Movie
    template_name = 'Movies/details.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView,self).get_context_data(**kwargs)
        context["meta"] = Cast.objects.all().filter(movie_id =self.object.pk)
        return context

class MovieCreate(CreateView):
    model = Movie
    fields = ['name','director','genre','movie_poster']