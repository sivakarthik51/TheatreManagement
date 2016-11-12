from django import forms
from models import Ticket
from Movies.models import Show,Movie
from Establishments.models import Establishment,Theatre

class TicketForm(forms.ModelForm):

    class Meta:
        model=Ticket
        fields = [ 'theatre','show', 'seat_no']

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('mov_id',None)
        print self.id
        movie = Movie.objects.get(pk=self.id)
        print Show.objects.filter(movie=movie)
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['show'].queryset = Show.objects.filter(movie=movie)

class MovieCreateForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = ['theatre', 'name', 'director', 'genre', 'movie_poster']

    def __init__(self,*args,**kwargs):
        self.establishment_user = kwargs.pop('establishment_user',None)
        print self.establishment_user
        if self.establishment_user:
            est = Establishment.objects.get(user=self.establishment_user)
        super(MovieCreateForm, self).__init__(*args, **kwargs)
        if self.establishment_user:
            self.fields['theatre'].queryset = Theatre.objects.filter(establishment__user=est)
