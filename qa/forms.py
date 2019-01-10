from django import forms
from .models import Question, Answer

class NewQuestionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), help_text='Maximum length of text: 3500 characters.', max_length=3500)

    class Meta:
        model = Question
        fields = ['subject', 'description']

class PostForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['message', ]
