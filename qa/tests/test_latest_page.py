from django.urls import reverse, resolve
from django.test import TestCase
from qa.models import Topic, Question, Answer
from qa.views import TopicsView
from django.utils import timezone
from django.contrib.auth.models import User
from qa.views import latest

# Tests the homepage of the application
class LatestPageTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name='QMConnect+', description='University topic.')
        self.user = User.objects.create_user(username='pit', email='pit@gmail.com', password='tiptiP161!')
        self.question = Question.objects.create(subject='What is QMConnect?', last_updated=timezone.now(), topic = self.topic, starter=self.user, views=0)
        self.answer = Answer.objects.create(message="Test", question=self.question, created_at=timezone.now(), created_by=self.user)
        # Get the url to the homepage
        self.url = reverse('qa:latest')
        # Get the response
        self.response = self.client.get(self.url)

    """
    Tests that the webpage returns the
    HTTP response code 200
    """
    def test_response_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    """
    Tests that the correct view is returned when
    accessing the webpage
    """
    def test_returned_view(self):
        # Retrieve the view function used when accessing the homepage
        view = resolve("/")
        # Tests that the view functions match
        self.assertEquals(view.func, latest)

    def test_home_view_contains_link_to_question(self):
        print(self.response.content)
        topic_questions_url = reverse('qa:question_answers', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk})
        self.assertContains(self.response, topic_questions_url)
