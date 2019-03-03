from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Topic, Question, Answer
from ..views import AnswerUpdateView
