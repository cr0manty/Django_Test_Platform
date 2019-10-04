from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    birth_date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        label='Дата рождения',
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    about_me = forms.CharField(
        label='О себе',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    def get_user(self):
        cd = self.cleaned_data
        user = User(
            username=cd.get('username'),
            email=cd.get('email'),
            first_name=cd.get('first_name'),
            last_name=cd.get('last_name')
        )
        user.set_password(cd.get('password'))
        profile = Profile(
            user=user,
            birth_date=self.birth_date,
            about=self.about_me
        )
        return profile

    def clean(self):
        super().clean()
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password_confirm'):
            self.add_error('password_confirm', 'Пароли не совпадают!')
        return cd


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
