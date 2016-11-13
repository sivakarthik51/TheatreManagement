from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.views.generic import View,RedirectView
from .forms import UserForm,LoginForm

class UserFormView(View):
    form_class = UserForm
    template_name = 'Login/registration_form.html'

    #display Blank Form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    # Process Form Data
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['confirm_password']
            if len(password) < 8:
                form.add_error('password',ValidationError('Password too short'))
                return render(request, self.template_name, {'form': form})
            if password != password1:
                form.add_error('confirm_password',ValidationError('Password does not match'))
                return render(request, self.template_name, {'form': form})
            user.set_password(password)

            user.save()
            user.groups.add(Group.objects.get(name='NormalUser'))

            # Return User Object if Credentials are correct
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('Home:home_index')
        return render(request,self.template_name,{'form':form})

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
        return redirect('Home:home_index')


