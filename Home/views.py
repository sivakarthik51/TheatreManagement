from django.shortcuts import render
from django.views import generic,View
from Movies.models import Movie
from Establishments.models import Establishment
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'Home/index.html'

    def get_queryset(self):
        return Movie.objects.all()

class AboutView(View):
    template_name = 'Home/about.html'
    establishments = Establishment.objects.all()
    def get(self,request):
        return render(request,self.template_name,{'establishments':self.establishments})