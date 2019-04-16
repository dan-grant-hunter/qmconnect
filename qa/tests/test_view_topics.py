from django.urls import reverse, resolve
from django.test import TestCase
from qa.models import Topic, Question, Answer
from qa.views import TopicsView
from django.utils import timezone
from django.contrib.auth.models import User

class TopicsTests(TestCase):
    """
    Having url and response in this method
    allows the tests to reuse the same response
    in a new test.
    """
    def setUp(self):
        self.topic = Topic.objects.create(name='QMConnect+', description='University topic.')
        self.user = User.objects.create_user(username='pit', email='pit@gmail.com', password='tiptiP161!')
        self.question = Question.objects.create(subject='What is QMConnect?', last_updated=timezone.now(), topic = self.topic, starter=self.user, views=0)
        self.answer = Answer.objects.create(message="Test", question=self.question, created_at=timezone.now(), created_by=self.user)
        url = reverse('qa:home')
        self.response = self.client.get(url)

    """
    Test if the response code returned is 200
    """
    def test_home_view_status_code_200(self):
        self.assertEquals(self.response.status_code, 200)

    """
    The resolve function makes sure the URL /topics/
    is returning the home view.
    """
    def test_home_url_resolves_home_view(self):
        view = resolve('/topics/')
        self.assertEquals(view.func.view_class, TopicsView)

    """
    assertContains tests if the response body contains the
    topic questions url
    """
    def test_home_view_contains_link_to_questions_page(self):
        topic_questions_url = reverse('qa:topic_questions', kwargs={'pk': self.topic.pk})
        self.assertContains(self.response, topic_questions_url)

    """
    Tests if the web page contains the url to the most popular question
    """
    def test_topics_page_contains_popular_question(self):
        popular_question_url = reverse('qa:question_answers', kwargs={'pk': self.topic.pk, 'question_pk': self.question.pk})
        self.assertContains(self.response, popular_question_url)
