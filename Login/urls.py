from . import views
from django.conf.urls import url

app_name = 'Login'

urlpatterns = [
    url(r'^$',views.UserFormView.as_view(),name='register')
]