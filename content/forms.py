from django import forms
from .models import Progress, News, City
from django.forms import ModelForm, TextInput


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['name', 'progress']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={
            'class': 'form-control',
            'name': 'city',
            'id': 'city',
            'placeholder': 'Введите город'
        })}