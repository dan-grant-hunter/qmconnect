from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Topic, Question, Answer
from ..views import AnswersView

class QuestionAnswersTest(TestCase):
    def setUp(self):
        topic = Topic.objects.create(name='QMConnect+', description='A platform for students from students.')
        user = User.objects.create_user(username='pit', email='pit@gmail.com', password='tiptiP161!')
        question = Question.objects.create(subject='Hello, QMConnect+!', topic=topic, starter=user)
        Answer.objects.create(message='Hello to you too!', question=question, created_by=user)
        url = reverse('qa:question_answers', kwargs={'pk': topic.pk, 'question_pk': question.pk})
        self.response = self.client.get(url)

    '''
    Tests the response status code.
    '''
    def test_response_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    '''
    Tests if it returns the proper view.
    '''
    def test_view_function(self):
        view = resolve('/topics/1/questions/1/')
        self.assertEquals(view.func.view_class, AnswersView)
