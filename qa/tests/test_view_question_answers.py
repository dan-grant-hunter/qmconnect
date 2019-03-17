from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from qa.models import Topic, Question, Answer
from qa.views import AnswersView

class QuestionAnswersTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name='QMConnect+', description='A platform for students from students.')
        self.user = User.objects.create_user(username='pit', email='pit@gmail.com', password='tiptiP161!')
        self.question = Question.objects.create(subject='Hello, QMConnect+!', topic=self.topic, starter=self.user)
        self.answer = Answer.objects.create(message='Hello to you too!', question=self.question, created_by=self.user)
        url = reverse('qa:question_answers', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk})
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

    '''
    Tests if the response contains the edit button
    '''
    def test_has_edit_button(self):
        # get the url to the answers web page
        question_answers_url = reverse('qa:question_answers', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk})
        # get the url of the edit button
        edit_url = reverse('qa:modify_answer', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk, 'answer_pk': self.answer.pk})
        # the edit url only appears if the user is logged in
        # log the user in
        self.client.login(username='pit', password='tiptiP161!')
        # get the response from the answers web page
        response = self.client.get(question_answers_url)
        self.assertContains(response, 'href="{0}"'.format(edit_url))

    '''
    Tests if the edit button is hidden if the user is not logged in
    '''
    def test_edit_button_is_hidden_from_unlogged_users(self):
        # get the url to the answers web page
        question_answers_url = reverse('qa:question_answers', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk})
        # get the url of the edit button
        edit_url = reverse('qa:modify_answer', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk, 'answer_pk': self.answer.pk})
        # get the response from the answers web page
        response = self.client.get(question_answers_url)
        self.assertNotContains(response, 'href="{0}"'.format(edit_url))

    '''
    Tests if the edit button is hidden from all other users
    except the one who the answer belongs to
    '''
    def test_edit_button_is_hidden_from_unlaogged_users(self):
        # get the url to the answers web page
        question_answers_url = reverse('qa:question_answers', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk})
        # get the url of the edit button
        edit_url = reverse('qa:modify_answer', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk, 'answer_pk': self.answer.pk})
        # the edit url only appears if the user is logged in
        # and if the answer belongs to the user
        # log in another user (not the one the answer belongs it)
        self.client.login(username='catalin', password='tiptiP161!')
        # get the response from the answers web page
        response = self.client.get(question_answers_url)
        self.assertNotContains(response, 'href="{0}"'.format(edit_url))
