from django.conf.urls import url
from . import views

app_name = 'Movies'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name='index'),

    #/movies/<id>/
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),

    #/movies/
    url(r'add/$',views.MovieCreate.as_view(),name = 'movie_add'),

    #/movies/edit/<id>
    url(r'edit/(?P<pk>[0-9]+)$',views.MovieUpdate.as_view(),name='movie_update'),

    #/movies/edit/<id>/delete
    url(r'edit/(?P<pk>[0-9]+)/delete$',views.MovieDelete.as_view(),name='movie_delete'),

    #/movies/book/<id>
    url(r'book/(?P<pk>[0-9]+)/$',views.BookTickets.as_view(),name='book_ticket'),

    #/movies/book/ticket/<id>
    url(r'book/ticket/(?P<pk>[0-9]+)/$',views.TicketDetailView.as_view(),name='ticket_details'),

    #/movies/theater
    url(r'theatre/$',views.ListMovies_Theatres.as_view(),name='theatre_specific')
]