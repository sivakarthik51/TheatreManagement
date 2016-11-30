from django.shortcuts import render,redirect
from django.views import generic,View
from django.views.generic import CreateView,UpdateView,DeleteView
from django.core.exceptions import ValidationError
from Movies.models import Movie
from Establishments.models import Establishment,Employee,Theatre
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from forms import EmployeeForm
from django.core.urlresolvers import reverse_lazy
# Create your views here.
class EmployeeIndexView(PermissionRequiredMixin,LoginRequiredMixin,generic.ListView):
    permission_required = 'Movies.add_movie'
    login_url = 'Login:register'
    template_name = 'Establishments/index.html'
    redirect_field_name = None
    context_object_name = 'all_Employees'

    def get_queryset(self):
        if self.request.user:
            return Employee.objects.filter(theatre__establishment__user=self.request.user)
        else:
            return None

class EmployeeCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
    permission_required = 'Movies.add_movie'
    permission_denied_message = 'Forbidden'
    login_url = 'Login:register'
    redirect_field_name = None
    form_class = EmployeeForm
    template_name = 'Establishments/employee_form.html'
    title="Add Employee For "
    def get(self,request):
        form = self.form_class(request.GET,estb_usr = request.user)
        self.title = self.title + str(Establishment.objects.get(user=request.user))
        return render(request, self.template_name, {'form': form, 'ti': self.title})

    def post(self,request):
        form = self.form_class(request.POST,estb_usr=request.user)
        self.title = self.title + str(Establishment.objects.get(user=request.user))
        if form.is_valid():

            emp = form.save(commit=False)

            if any(not char.isalpha() for char in emp.name):
                form.add_error('name', ValidationError('Name can Contain only alphabets'))
                return render(request, self.template_name, {'form': form, 'ti': self.title})
            print "Saving Form"
            form.save()
            return redirect('Establishments:employee_index')
        return render(request, self.template_name, {'form': form, 'ti': self.title})

class EmployeeUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    permission_required = 'Movies.add_movie'
    permission_denied_message = 'Forbidden'
    login_url = 'Login:register'
    redirect_field_name = None
    model = Employee
    fields = ['name', 'theatre', 'Role']

class EmployeeDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    permission_required = 'Movies.add_movie'
    permission_denied_message = 'Forbidden'
    login_url = 'Login:register'
    redirect_field_name = None
    model = Employee
    success_url = reverse_lazy('Establishments:employee_index')