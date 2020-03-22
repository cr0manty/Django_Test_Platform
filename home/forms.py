from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'birth_date')
        widgets = {'checkin': forms.DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

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
