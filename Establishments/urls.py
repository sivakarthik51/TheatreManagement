from django.conf.urls import url
from . import views

app_name = 'Establishments'

urlpatterns = [
    url(r'^employee/$', views.EmployeeIndexView.as_view(),name='employee_index'),
    url(r'^employee/add$', views.EmployeeCreate.as_view(),name='employee_create'),
    url(r'^employee/edit/(?P<pk>[0-9]+)$', views.EmployeeUpdate.as_view(),name='employee_edit'),
    url(r'^employee/edit/(?P<pk>[0-9]+)/delete$', views.EmployeeDelete.as_view(),name='employee_delete'),

]