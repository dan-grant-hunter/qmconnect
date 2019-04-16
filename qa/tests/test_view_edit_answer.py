from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import resolve, reverse
from qa.models import Topic, Question, Answer
from qa.views import AnswerUpdateView
