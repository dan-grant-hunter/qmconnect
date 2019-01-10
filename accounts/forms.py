from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
from datetime import date

class RegisterForm(UserCreationForm):
    email = forms.CharField(
                    max_length=254,
                    required=True,
                    widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget = (forms.widgets.DateInput(format="%m/%d/%Y", attrs={'placeholder':'mm/dd/yyyy'})))

    class Meta:
        model = Profile
        fields = ('dob',)
