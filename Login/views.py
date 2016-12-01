from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.views.generic import View,RedirectView
from .forms import UserForm,LoginForm
from django.core.validators import validate_email
from models import UserWallet
from django.contrib.auth.mixins import LoginRequiredMixin
from Movies.models import Ticket

class UserFormView(View):
    form_class = UserForm
    template_name = 'Login/registration_form.html'
    ti = 'Create New Account'
    #display Blank Form
    def get(self,request):
        form = self.form_class(None)
        ti = 'Create New Account'
        return render(request,self.template_name,{'form':form,'ti':ti})

    # Process Form Data
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['confirm_password']
            if any(not char.isalpha() for char in user.first_name):
                form.add_error('first_name', ValidationError('Name can Contain only alphabets'))
                return render(request, self.template_name, {'form': form, 'ti': self.ti})

            if any(not char.isalpha() for char in user.last_name):
                form.add_error('last_name', ValidationError('Name can contain only alphabets'))
                return render(request, self.template_name, {'form': form, 'ti': self.ti})

            if User.objects.filter(email = user.email).exists():
                form.add_error('email',ValidationError('Another user has registered with the same email address'))
                return render(request, self.template_name, {'form': form, 'ti': self.ti})

            if  validate_email(user.email):
                form.add_error('email', ValidationError('Please enter a valid email address'))
                return render(request, self.template_name, {'form': form, 'ti': self.ti})

            if len(password) < 8:
                form.add_error('password',ValidationError('Password too short(Minimum 8 characters)'))
                return render(request, self.template_name, {'form': form, 'ti': self.ti})

            if password != password1:
                form.add_error('confirm_password',ValidationError('Password does not match'))
                return render(request, self.template_name, {'form': form, 'ti': self.ti})



            user.set_password(password)
            user.save()
            usrwlt = UserWallet()
            usrwlt.user = user
            usrwlt.save()

            user.groups.add(Group.objects.get(name='NormalUser'))

            # Return User Object if Credentials are correct
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    if request.user.groups.filter(name='Establishment').exists():
                        return redirect('Movies:theatre_specific')
                    else:
                        return redirect('Movies:index')
        return render(request,self.template_name,{'form':form,'ti':self.ti})

class Logout(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
            request.user=None
        return redirect('Home:home_index')

class Login(View):
    form_class = LoginForm
    template_name = 'Login/login.html'

    def post(self,request):
        form = self.form_class(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if not request.user.is_authenticated:
            if user is not None:
                if user.is_active:
                    login(request,user)
                    if request.user.groups.filter(name='Establishment').exists():
                        return redirect('Movies:theatre_specific')
                    else:
                        return redirect('Movies:index')

        return redirect('Login:register')

class Dashboard(LoginRequiredMixin,View):
    redirect_field_name = None
    login_url = 'Login:register'
    template_name = 'Login/dashboard.html'

    def get(self,request):
        tickets = Ticket.objects.filter(user=self.request.user)
        return render(request,self.template_name,{'usr':request.user,'tickets':tickets})