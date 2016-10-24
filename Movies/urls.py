from django.conf.urls import url
from . import views

app_name = 'Movies'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name='index'),

    #/movies/<id>/
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),

    #/movies/
    url(r'add/$',views.MovieCreate.as_view(),name = 'movie_add'),
]