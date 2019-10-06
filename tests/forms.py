from django import forms
from django.core.exceptions import ValidationError

from .models import Test, Comment, Question


class TestForm(forms.ModelForm):
    author = None

    class Meta:
        model = Test
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название',
            'description': 'Описание',
        }

        def clean_slug(self):
            new_slug = self.cleaned_data.get('slug').lower()
            if new_slug == 'create' or new_slug == 'filter':
                raise ValidationError('Slug may not be create')
            return new_slug


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'text': 'Текст',
        }


class QuestionForm(forms.Form):
    question_list = []
    question = forms.CharField(
        label='Вопрос',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вопрос'
        })
    )
    answer_1 = forms.CharField(
        label='Ответ 1',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ответ'
        })
    )
    answer_2 = forms.CharField(
        label='Ответ 2',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ответ'
        })
    )
    answer_3 = forms.CharField(
        label='Ответ 3',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ответ'
        })
    )
    answer_4 = forms.CharField(
        label='Ответ 4',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ответ'
        })
    )

    def get_answers(self):
        cd = self.cleaned_data
        return '{};{};{};{}'.format(cd.get('answer_1'), cd.get('answer_2'),
                                       cd.get('answer_3'), cd.get('answer_4'))
