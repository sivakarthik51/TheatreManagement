from .models import Movie,Cast,Movie_Meta,Ticket,Show
from Establishments.models import Theatre,Establishment
from Login.models import UserWallet
from datetime import datetime
from django.core.exceptions import ValidationError
import imdb
from django.db.models import Min, Max
from django.core.mail import EmailMessage
from .forms import TicketForm,MovieCreateForm,MovieQueryForm
from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import View,ListView
from django.db import transaction
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from forms import ShowForm
import dateutil.parser
class IndexView(generic.ListView):
    template_name = 'Movies/index.html'
    context_object_name = 'all_Movies'
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['can_change'] = False
        return context
    def get_queryset(self):
        return get_distinct_movies()

def get_distinct_movies():
    movies = Movie.objects.all()
    checked = []
    movies_new = []
    for movie in movies:
        if not (movie.name in checked):
            movies_new.append(movie)
        checked.append(movie.name)
    print movies_new
    return movies_new

class DetailView(generic.DetailView):
    model = Movie
    template_name = 'Movies/details.html'
    def get_context_data(self, **kwargs):
        context = super(DetailView,self).get_context_data(**kwargs)
        context["meta"] = Cast.objects.all().filter(movie_id =self.object.pk)
        context["mov_meta"] = Movie_Meta.objects.all().filter(movie_id=self.object.pk).first()
        theatres=[]
        t = Movie.objects.get(pk = self.object.pk)
        movies = Movie.objects.all()
        for movie in movies:
            if movie.name == t.name:
                theatres.append(Theatre.objects.get(pk=movie.theatre.id))
        if self.request.user and self.request.user.groups.filter(name='Establishment').exists():
            for th in theatres:
                print th.establishment.user
                if not( th.establishment.user == self.request.user):
                    theatres.remove(th)

        context["theatres"]=theatres
        temp3 = Show.objects.filter(movie__name = self.object.name)
        temp1 = temp3.filter(show_time__gte=datetime.now())
        print temp3
        print temp1
        context["shows"] = Show.objects.filter(movie__name = self.object.name,show_time__gte=datetime.now()) #.filter(movie = self.object)
        return context
"""
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
                    metadata.runtime= str(filter(str.isdigit,movie.get('runtime')))
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


class MovieCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
    permission_required = 'Movies.add_movie'
    permission_denied_message = 'Forbidden'
    login_url = 'Login:register'
    redirect_field_name = None
    form_class = MovieCreateForm
    template_name = 'Movies/movie_form.html'
    title="Add Movie"
    def get(self,request):
        form = self.form_class(request.GET,establishment_user=request.user)
        return render(request, self.template_name, {'form': form,'ti':self.title})

    def post(self, request):
        print request.user
        form = self.form_class(request.POST,request.FILES,establishment_user=request.user)
        print request.FILES
        if form.is_valid():


            try:
                movie_form = form.save(commit=False)
                ia = imdb.IMDb()
                if movie_form.meta_completed is False:
                    s_result = ia.search_movie(movie_form.name)
                    print s_result[0]
                    if not str(s_result[0]).__contains__(movie_form.name) :
                        form.add_error('name',ValidationError('Movie Does Not Exist'))
                        print "Movie Does not Exist"
                        return render(request, self.template_name, {'form': form})
                    print s_result
                    movieID = s_result[0].movieID
                    movie = ia.get_movie(movieID)
                    dir = movie.get('director')
                    flag_director = False
                    flag_genre = False
                    for i in range(0,len(dir)):
                        print dir[i]
                        if str(movie_form.director) == str(dir[i]):
                            print "Correct Director"
                            flag_director = True
                            break
                    genres = movie.get('genres')
                    for i in range(0,len(genres)):
                        if str(movie_form.genre) == str(genres[i]):
                            flag_genre = True
                            break

                    if not flag_director:
                        form.add_error('director',ValidationError('Wrong Director'))
                        return render(request, self.template_name, {'form': form})
                    if not flag_genre:
                        form.add_error('genre', ValidationError('Incorrect Genre'))
                        return render(request, self.template_name, {'form': form})
                    people = movie.get('cast')
                    rating = movie.get('rating')
                    movie_form.meta_completed = True
                    movie_form.save()
                    metadata = Movie_Meta()
                    metadata.movie= movie_form
                    metadata.rating = rating
                    metadata.release_date = str(movie.get('year'))
                    metadata.runtime= str(filter(str.isdigit,movie.get('runtime')))

                    metadata.save()
                    topActors = 5
                    for actor in people[:topActors]:
                        cast = Cast()
                        cast.movie=movie_form
                        cast.person_name = actor['name']
                        cast.character_name = actor.currentRole
                        cast.save()
                        print "Cast Saved"


                    print "Movie saved"
                    return redirect('Movies:detail',pk=movie_form.pk,)
            except Exception as e:
                print e
                return render(request, self.template_name, {'form': form,'ti':self.title})
        print "invalid Form"
        return render(request, self.template_name, {'form': form,'ti':self.title})

#create View End

class MovieUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    permission_required = 'Movies.add_movie'
    permission_denied_message = 'Forbidden'
    login_url = 'Login:register'
    redirect_field_name = None
    model = Movie
    fields = ['name', 'director', 'genre', 'movie_poster']





class MovieDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    permission_required = 'Movies.add_movie'
    permission_denied_message = 'Forbidden'
    login_url = 'Login:register'
    redirect_field_name = None
    model = Movie
    success_url = reverse_lazy('Movies:index')

class BookTickets(LoginRequiredMixin,CreateView):
    login_url = 'Login:register'
    redirect_field_name = None
    form_class = TicketForm
    template_name = 'Movies/ticket_form.html'
    title = 'Book Tickets'
    def get_context_data(self,*args, **kwargs):
        print Movie.objects.get(pk=self.request.pk).max_no_seats
        context = super(BookTickets, self).get_context_data(*args,**kwargs)
        print Movie.objects.get(pk=self.request.pk).max_no_seats
        context["ticket_range"] = Movie.objects.get(pk=self.request.pk).max_no_seats
        return context


    def get(self,request,pk):

        form = self.form_class(None)
        return render(request,self.template_name,{'form':form,'pk':pk,'ti':self.title})

    def post(self,request,pk):
        max_seats= Movie.objects.get(pk=pk).max_no_seats
        tickets = Ticket.objects.filter(movie=Movie.objects.get(pk = pk))
        shows = Show.objects.filter(movie__name=Movie.objects.get(pk=pk).name,show_time__gte=datetime.now())
        form = self.form_class(request.POST,mov_id=pk)
        if form.is_valid():
            ticket = form.save(commit=False)

            ticket.user = request.user
            ticket.movie = Movie.objects.get(pk = pk)
            #Ticket numbers taken for the shows
            nos = []
            tis = Ticket.objects.filter(movie=Movie.objects.get(pk=pk),show=ticket.show)
            for t in tis:
                nos.append(t.seat_no)
            if ticket.seat_no in nos:
                form.add_error('seat_no','Seat Already taken')
                return render(request, self.template_name, {'form': form,'seats':range(max_seats),'tickets':tickets,'shows':shows,'ti':self.title})
            cred = UserWallet.objects.get(user=request.user)
            if cred.credit-ticket.price < 0:
                form.add_error('seat_no','Please restock your account before Booking tickets')
                return render(request, self.template_name,
                              {'form': form, 'seats': range(max_seats), 'tickets': tickets, 'shows': shows,
                               'ti': self.title})
            cred.credit = cred.credit - ticket.price
            cred.save()

            ticket.theatre = Theatre.objects.get(pk=ticket.show.theatre_id)
            msg1 = 'Hi ' + str(
                ticket.user) + '!\n\nYour ticket booking has been confirmed, with the following details : \n'
            msg2 = 'Movie : ' + str(ticket.movie) + '\nTheatre : ' + str(ticket.theatre) + '\nShow : ' + str(
                ticket.show) + '\nSeat Number : ' + str(ticket.seat_no)
            msg3 = '\nPrice : Rs.' + str(ticket.price)
            msg4 = '\nRemaining Credit: Rs.' +str(cred.credit)
            msg5 = '\n\nThank you for choosing TheatriX, Enjoy your movie!'
            msg = msg1 + msg2 + msg3 + msg4 + msg5
            email = EmailMessage('Your tickets for ' + str(ticket.movie.name), msg,
                                 'TheatriX.BookingConfirmation@gmail.com', [ticket.user.email])
            try:
                if email.send():
                    print "Email Sent"
                else:
                    print "Email Not sent"
            except Exception as e:
                print e
            ticket.save()
            return redirect('Movies:ticket_details',pk=ticket.pk)
        return render(request, self.template_name, {'form': form,'seats':range(max_seats),'tickets':tickets,'shows':shows,'ti':self.title})

class ListMovies_Theatres(UserPassesTestMixin,LoginRequiredMixin,ListView):

    def test_func(self):
        can_change = self.request.user.groups.filter(name='Establishment').exists()
        print can_change
        return can_change
    can_change = True
    model = Movie
    login_url = '/'
    redirect_field_name = None
    template_name = 'Movies/index.html'
    context_object_name = 'all_Movies'

    def get_context_data(self, **kwargs):
        context = super(ListMovies_Theatres, self).get_context_data(**kwargs)
        context['can_change'] = self.request.user.groups.filter(name='Establishment').exists()
        return context
    def get_queryset(self):
        user = self.request.user
        print user
        print Movie.objects.filter(theatre__establishment__user=user)
        return Movie.objects.filter(theatre__establishment__user=user)




class TicketDetailView(LoginRequiredMixin,generic.DetailView):
    login_url = 'Login:register'
    redirect_field_name = None
    model=Ticket
    template_name = 'Movies/ticket_details.html'


    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context["mov_meta"] = Movie_Meta.objects.all().filter(movie_id=self.object.movie.id).first()
        return context

class MovieQueries(generic.ListView):
    login_url = '/'
    redirect_field_name = None
    model = Movie
    template_name = 'Movies/index.html'
    context_object_name = 'all_movies'
    form_class = MovieQueryForm
    def post(self,request):
        form = self.form_class(request.POST)
        query = request.POST.get('query')
        filter_condition = request.POST.get('filter_condition')
        if filter_condition == str(0):
            if len(query) > 2:
                movies = Movie.objects.filter(name__contains=query)
                distinct = []
                checked = []
                for movie in movies:
                    if not movie.name in checked:
                        distinct.append(movie)
                    checked.append(movie.name)
                print distinct
                return render(request, self.template_name, {'all_Movies': distinct})
            return redirect('Movies:index')
        if filter_condition == str(1):
            print "res"
            movies= Movie.objects.filter(theatre__city__contains=query)
            distinct = []
            checked = []
            for movie in movies:
                if not movie.name in checked:
                    distinct.append(movie)
                checked.append(movie.name)
            print distinct
            return render(request, self.template_name,{'all_Movies':distinct})
        if filter_condition == str(2):
            theatres = Theatre.objects.filter(name=query)
            movies = Movie.objects.filter(theatre__name__contains=query)
            distinct = []
            checked = []
            for movie in movies:
                if not movie.name in checked:
                    distinct.append(movie)
                checked.append(movie.name)
            print distinct
            return render(request, self.template_name, {'all_Movies': distinct})
        if filter_condition == str(3):
            if len(query)>2:
                movies = Movie.objects.filter(theatre__location__contains=query)
                distinct = []
                checked = []
                for movie in movies:
                    if not movie.name in checked:
                        distinct.append(movie)
                    checked.append(movie.name)
                return render(request, self.template_name, {'all_Movies': distinct})
            else:
                print "validation error"
                form.add_error('query',ValidationError('Cannot search with small parameters'))
                return render(request, self.template_name, {'form': form})
        if filter_condition == str(4):
            if len(query)>2:
                movies = Movie.objects.filter(genre__contains=query)
                distinct = []
                checked = []
                for movie in movies:
                    if not movie.name in checked:
                        distinct.append(movie)
                    checked.append(movie.name)
                return render(request, self.template_name, {'all_Movies': distinct})
            else:
                print "validation error"
                form.add_error('query',ValidationError('Cannot search with small parameters'))
                return render(request, self.template_name, {'form': form})


class CreateShow(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'Login:register'
    redirect_field_name = None
    permission_required = 'Movies.add_movie'
    form_class = ShowForm
    template_name = 'Movies/show_form.html'

    def get(self,request,pk):
        form = self.form_class(request.GET,mov_id = pk,establishment_user=request.user)
        title = "Create Show for "+str(Movie.objects.get(pk = pk).name)
        return render(request,self.template_name,{'form':form,'pk':pk,'ti':title})

    def post(self,request,pk):
        form = self.form_class(request.POST,mov_id = pk,establishment_user=request.user)
        title = "Create Show for " + str(Movie.objects.get(pk=pk).name)

        #request.POST['show_time'] = dateutil.parser.parse(request.POST['show_time_0'] + " " + request.POST['show_time_1'])


        print form.is_valid()
        if form.is_valid():
            try:
                print "Inside"
                show = form.save(commit=False)
                show.movie = Movie.objects.get(pk=pk)
                if show.show_time < datetime.now():
                    form.add_error('show_time',ValidationError('Time must be after this moment'))
                    return render(request, self.template_name, {'form': form, 'pk': pk, 'ti': title})
                show.save()
            except Exception as e:
                print e

            return redirect('Movies:detail', pk=pk, )
        return render(request, self.template_name, {'form': form, 'pk': pk,'ti':title})