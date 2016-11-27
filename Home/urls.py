from django.conf.urls import url
from . import views

app_name = 'Home'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),name='home_index'),
    url(r'^about/$', views.AboutView.as_view(),name='about'),
]