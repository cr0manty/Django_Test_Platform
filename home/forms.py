from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    password_confirm = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password_confirm', 'birth_date')
        widgets = {'checkin': forms.DateInput(), 'password': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.PasswordInput()

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

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
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')

        user = User.objects.filter(username=username).first()
        if user is not None and not user.check_password(password):
            raise forms.ValidationError('Пароль и имя пользователя не совпадают')
        return super().clean()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).count():
            raise forms.ValidationError('Пользователь с таким логином еще не зарегестрирован')
        return username


class ImageForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'accept': '.png, .jpg, .jpeg',
            'onchange': 'submit();'
        }),
    )
