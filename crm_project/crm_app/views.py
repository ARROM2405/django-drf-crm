from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .forms import *


class RegisterView(generic.View):
    form = RegistrationForm

    def get(self, request, form=form):
        return render(request, 'crm_app/registration.html', context={'form': form})

    def post(self, request, form=form):
        form = form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(username, raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home_page')
        return render(request, 'crm_app/registration.html', context={'form': form})


class UserLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'crm_app/login.html'

    def get_success_url(self):
        return reverse('home_page')


class HomePageView(generic.View):
    def get(self, request):
        return render(request, 'crm_app/home_page.html')



