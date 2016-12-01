from django import forms
from models import Ticket
from django.contrib.admin import widgets
from Movies.models import Show,Movie
from Establishments.models import Establishment,Theatre
from datetimewidget.widgets import DateTimeWidget
import dateutil.parser
from datetime import datetime


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
        self.fields['show'].queryset = Show.objects.filter(movie__name=movie.name,show_time__gte=datetime.now())
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


class ShowForm(forms.ModelForm):
    show_time = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    # show_time = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())
    class Meta:
        model = Show
        fields=['show_time','price','theatre']
        #exclude = ('show_time',)

    def clean(self):
        super(ShowForm, self).clean()
        #show_time = " ".join(self.cleaned_data['show_time'])


    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('mov_id',None)
        self.eu = kwargs.pop('establishment_user',None)
        print self.id
        print self.eu
        super(ShowForm, self).__init__(*args, **kwargs)
        movie = Movie.objects.get(pk=self.id)
        print Theatre.objects.filter(movie=movie).filter(establishment__user=self.eu)
        #self.fields['show_time'].widget = widgets.AdminSplitDateTime()
        self.fields['theatre'].queryset = Theatre.objects.filter(movie=movie).filter(establishment__user=self.eu)


