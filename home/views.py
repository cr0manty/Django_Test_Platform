from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate

from .forms import *


def home_page(request):
    return redirect('test_list')


class LoginUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'home/auth/login.html', context={
            'form': form
        })

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('user_redirect')
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
        return render(request, 'home/auth/login.html', context={
            'form': form
        })


class RegisterUser(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'home/auth/registration.html', context={
            'form': form
        })

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
        return render(request, 'home/auth/registration.html', context={
            'form': form
        })


class LogoutUser(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        logout(request)
        return redirect('home_url')


def show_user(request, username):
    user = get_object_or_404(User, username__iexact=username)
    return render(request, 'home/user.html', context={
        'user': user,
        'form': ImageForm()
    })


def redirect_to_user(request):
    if request.user.is_authenticated:
        return redirect('user_url', username=request.user)
    return redirect('login_url')


class SetAbout(View):
    def post(self, request, username):
        user = User.objects.filter(username=username).first()
        if user is not None:
            user.about = request.POST.get('about')
            user.save()
        return redirect('user_redirect')


class SetImage(View):
    def post(self, request, username):
        data = ImageForm(request.POST, request.FILES)
        if data.is_valid():
            image = data.cleaned_data.get('image')
            image._name = '{}_image.{}'.format(username, image._name.split('.')[-1])
            user = User.objects.filter(username=username).first()
            user.image = image
            user.save()
        return redirect('user_redirect')

