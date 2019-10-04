from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate

from .forms import *
from .models import Profile


def home_page(request):
    return render(request, 'home/index.html')


class LoginUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'home/auth/login.html', context={
            'form': form
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd.get('username', ''),
                password=cd.get('password', '')
            )
            if user is not None:
                login(request, user)
                return redirect('user_url', cd.get('username'))
            else:
                return redirect('login_url')
        return redirect('home_url')


class RegisterUser(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'home/auth/registration.html', context={
            'form': form
        })

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            user.save()
            return redirect('login_url')
        return redirect('registration_url')


class LogoutUser(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        logout(request)
        return redirect('home_url')


def show_user(request, username):
    user = get_object_or_404(Profile, user__username__iexact=username)
    return render(request, 'home/user.html', context={
        'user': user,
    })


def redirect_to_user(request):
    if request.user.is_authenticated:
        return redirect('user_url', username=request.user)
    return redirect('login_url')
