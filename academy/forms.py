from django import forms
from .models import Request

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Master, Client

class MasterSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Enter your full name')

    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        master = Master.objects.create(user=user, name=self.cleaned_data['name'])
        return user

class ClientSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Enter your full name')

    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        client = Client.objects.create(user=user, name=self.cleaned_data['name'])
        return user

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['master', 'description']
