from django import forms
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_username(value):
    user = User.objects.filter(username=value).first()
    if user is not None:
        raise ValidationError('Пользователь с таким логином уже зарегестрирован')


def validate_login(value):
    user = User.objects.filter(username=value).first()
    if user is None:
        raise ValidationError('Пользователь с таким логином еще не зарегестрирован')


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
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_username]
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[validate_email]
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
        input_formats=['%Y-%m-%d'],
        label='Дата рождения',
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def save(self):
        cd = self.cleaned_data
        user = User(
            username=cd.get('username'),
            email=cd.get('email'),
            first_name=cd.get('first_name'),
            last_name=cd.get('last_name'),
            birth_date=cd.get('birth_date')
        )
        user.set_password(cd.get('password'))
        user.save()

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
        validators=[validate_login]
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        super().clean()
        cd = self.cleaned_data
        user = User.objects.filter(username=cd.get('username')).first()
        if user is not None and not user.check_password(cd.get('password')):
            raise ValidationError('Пароль и имя пользователя не совпадают')
        return cd


class ImageForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'accept': '.png, .jpg, .jpeg',
            'onchange': 'submit();'
        }),
    )
