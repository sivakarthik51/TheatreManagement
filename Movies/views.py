from .models import Movie,Cast,Movie_Meta,Ticket,Show
import imdb
import smtplib
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .forms import TicketForm,MovieCreateForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import View
from django.db import transaction
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect

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
"""
class MovieCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
    permission_required = 'movies.can_add'
    permission_denied_message = 'Forbidden'
    login_url = '/'
    redirect_field_name = None
    model = Movie
    fields = ['theatre','name','director','genre','movie_poster']

    global mov
    mov = Movie.objects.all()

    transaction.on_commit(get_meta)
"""
#Create View TODO
class MovieCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
    permission_required = 'Movies.add_movie'
    permission_denied_message = 'Forbidden'
    login_url = '/'
    redirect_field_name = None
    form_class = MovieCreateForm
    template_name = 'Movies/movie_form.html'
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        print request.user
        form = self.form_class(request.POST,establishment_user=request.user)

        if form.is_valid():
            movie = form.save(commit = False)
            ia = imdb.IMDb()
            try:
                if movie.meta_completed is False:
                    s_result = ia.search_movie(movie.name)
                    if s_result is None:
                        print "Movie Does not Exist"
                        return render(request, self.template_name, {'form': form})
                    movieID = s_result[0].movieID
                    movie = ia.get_movie(movieID)
                    people = movie.get('cast')
                    rating = movie.get('rating')
                    metadata = Movie_Meta()
                    metadata.movie=movie
                    metadata.rating = rating
                    metadata.release_date = str(movie.get('year'))
                    metadata.runtime= movie.get('runtime')
                    metadata.save()
                    topActors = 5
                    for actor in people[:topActors]:
                        cast = Cast()
                        cast.movie=movie
                        cast.person_name = actor['name']
                        cast.character_name = actor.currentRole
                        cast.save()
                    movie.meta_completed = True
                    movie.save()
            except:
                print "Exception"
                pass


#create View End

class MovieUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    permission_required = 'movies.can_add'
    permission_denied_message = 'Forbidden'
    login_url = '/'
    redirect_field_name = None
    model = Movie
    fields = ['name', 'director', 'genre', 'movie_poster']

    global mov
    mov = Movie.objects.all()

    transaction.on_commit(get_meta)



class MovieDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    permission_required = 'movies.can_add'
    permission_denied_message = 'Forbidden'
    login_url = '/'
    redirect_field_name = None
    model = Movie
    success_url = reverse_lazy('Movies:index')

class BookTickets(LoginRequiredMixin,View):
    login_url = '/'
    redirect_field_name = None
    form_class = TicketForm
    template_name = 'Movies/ticket_form.html'

    def get(self,request,pk):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request,pk):
        form = self.form_class(request.POST,mov_id=pk)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.movie = Movie.objects.all().filter(pk = pk).first()

            email = EmailMessage('Booking Tickets '+str(ticket.movie.name),"Ticket Confirmed -- Seat No "+str(ticket.seat_no),'sivakarthik51@gmail.com',[ticket.user.email])
            try:
                if email.send():
                    print "Email Sent"
                else:
                    print "Email Not sent"
            except Exception as e:
                print e
            ticket.save()
            return redirect('Movies:index')
        return render(request, self.template_name, {'form': form})

class ListMovies_Theatres(View):
    #model = movie
    template_name = 'Movies/index.html'
    def get(self,request,id):
        return render(request,self.template_name,{'mov':Movie.objects.filter(theatre_id=id)})