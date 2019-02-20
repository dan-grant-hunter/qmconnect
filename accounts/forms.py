from django.contrib.auth.models import User
from .models import Profile, Message, Conversation
from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
from datetime import date

# registration form that is used for the User model
class RegisterForm(UserCreationForm):
    email = forms.CharField(
                    max_length=254,
                    required=True,
                    widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

# profile form that is used for the Profile model
class ProfileForm(forms.ModelForm):
    dob = forms.DateField(widget = (forms.widgets.DateInput(format="%m/%d/%Y", attrs={'placeholder':'mm/dd/yyyy'})))
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('image', 'dob',  'subject', 'universityYear', 'module', 'interest', )

# the form that is used to send a message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text', )

# the form that is used to send a message
class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ('members', )
