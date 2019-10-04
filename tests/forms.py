from django import forms
from django.core.exceptions import ValidationError

from .models import Test, Comment


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
            if new_slug == 'create':
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
    pass