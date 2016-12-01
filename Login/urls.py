from . import views
from django.conf.urls import url

app_name = 'Login'

urlpatterns = [
    url(r'^create/$',views.UserFormView.as_view(),name='register'),
    url(r'^logout/$',views.Logout.as_view(),name='logout'),
    url(r'^login/$',views.Login.as_view(),name='login_user'),
    url(r'^dashboard/$',views.Dashboard.as_view(),name='dashboard'),
]