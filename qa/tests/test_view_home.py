from django.urls import reverse, resolve
from django.test import TestCase
from ..models import Topic
from ..views import TopicsView

class HomeTests(TestCase):
    """
    Having url and response in this method
    allows the tests to reuse the same response
    in a new test.
    """
    def setUp(self):
        self.topic = Topic.objects.create(name='QMConnect+', description='University topic.')
        url = reverse(TopicsView)
        self.response = self.client.get(url)

    """
    The resolve function makes sure the URL /
    (root url) is returning the home view.
    """
    def test_home_view_status_code_200(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, TopicsView)

    """
    assertContains tests if the response body contains a given text
    The text used is the 'href' part of an 'a' tag (href="/topics/1/").
    """
    def test_home_view_contains_link_to_questions_page(self):
        topic_questions_url = reverse('QuestionsView', kwargs={'pk': self.topic.pk})
        self.assertContains(self.response, 'href="{0}"'.format(QuestionsView_url))
