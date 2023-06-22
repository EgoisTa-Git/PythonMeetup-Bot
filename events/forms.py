from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person


class PersonCreationForm(UserCreationForm):


    class Meta:
        model = Person
        fields = ('username', 'tg_id', 'role')


class PersonChangeForm(UserChangeForm):

    class Meta:
        model = Person
        fields = ('username', 'tg_id', 'role', 'bot_state', 'password')
