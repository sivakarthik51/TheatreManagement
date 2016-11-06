from .models import Movie,Cast,Movie_Meta
import imdb
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.db import transaction

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
        context["mov_meta"] = Movie_Meta.objects.all().filter(movie_id=self.object.pk).first()
        return context

mov = None

def get_meta():
    ia = imdb.IMDb()
    global mov
    if mov is not None:
        for t in mov:
            try:
                print "try"
                if t.meta_completed is False:
                    print "inside"
                    s_result = ia.search_movie(t.name)
                    movieID = s_result[0].movieID
                    movie = ia.get_movie(movieID)
                    people = movie.get('cast')
                    rating = movie.get('rating')
                    metadata = Movie_Meta()
                    metadata.movie=t
                    metadata.rating = rating
                    metadata.release_date = str(movie.get('year'))
                    metadata.runtime= movie.get('runtime')
                    metadata.save()
                    topActors = 5
                    for actor in people[:topActors]:
                        cast = Cast()
                        cast.movie=t
                        cast.person_name = actor['name']
                        cast.character_name = actor.currentRole
                        cast.save()
                    t.meta_completed = True
                    t.save()
            except:
                print "Exception"
                mov = None
                pass

class MovieCreate(LoginRequiredMixin,CreateView):
    login_url = '/'
    redirect_field_name = None
    model = Movie
    fields = ['name','director','genre','movie_poster']

    global mov
    mov = Movie.objects.all()

    transaction.on_commit(get_meta)

