from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


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
        input_formats=['%Y-%m-%d'],
        label='Дата рождения',
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        self.set_password(password)
        if commit:
            super().save()

    def clean_password_confirm(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')

        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if user is not None:
            raise forms.ValidationError('Пользователь с таким логином уже зарегестрирован')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        user = User.objects.filter(username=self.username).first()
        if user is not None and not user.check_password(self.password):
            raise forms.ValidationError('Пароль и имя пользователя не совпадают')
        return super().clean()

    def clean_username(self):
        user = User.objects.filter(username=self.username).first()
        if user is None:
            raise forms.ValidationError('Пользователь с таким логином еще не зарегестрирован')
        return self.username


class ImageForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'accept': '.png, .jpg, .jpeg',
            'onchange': 'submit();'
        }),
    )
