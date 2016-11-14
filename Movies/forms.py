from django import forms
from models import Ticket
from Movies.models import Show,Movie
from Establishments.models import Establishment,Theatre

class TicketForm(forms.ModelForm):

    class Meta:
        model=Ticket
        fields = ['show', 'seat_no']

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('mov_id',None)
        print self.id
        movie = Movie.objects.get(pk=self.id)
        print Show.objects.filter(movie=movie)
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['show'].queryset = Show.objects.filter(movie=movie)
        t = Movie.objects.values_list('theatre',flat=True).filter(name=movie.name)
        theatres = Theatre.objects.filter(pk__in=t)
        print t
        print theatres
        #self.fields['theatre'].queryset=theatres

class MovieCreateForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = [ 'theatre', 'name', 'director', 'genre', 'movie_poster']

    def __init__(self,*args,**kwargs):
        self.establishment_user = kwargs.pop('establishment_user',None)
        print self.establishment_user
        if self.establishment_user:
            est = Establishment.objects.get(user=self.establishment_user)
        super(MovieCreateForm, self).__init__(*args, **kwargs)
        #self.fields['movie_poster'].required = False
        print est.name
        if self.establishment_user:
            self.fields['theatre'].queryset = Theatre.objects.filter(establishment=est)

class MovieQueryForm(forms.ModelForm):
    query = forms.CharField(max_length = 255)
    class Meta:
        model=Movie
        fields=['theatre']

#TODO Show Form
class ShowForm(forms.ModelForm):
    show_time = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Show
        fields=['show_time','theatre']

    def __init__(self, *args, **kwargs):
        #self.id = kwargs.pop('mov_id',None)
        #self.eu = kwargs.pop('establishment_user',None)
        #print self.id
        #print self.eu
        super(ShowForm, self).__init__(*args, **kwargs)
        #movie = Movie.objects.get(pk=self.id)
        #self.fields['theatre'].queryset = Theatre.objects.filter(movie=movie).filter(establishment__user=self.eu)


