from django.urls import resolve, reverse
from django.test import TestCase
from qa.models import Topic
from qa.views import QuestionsView

'''
Code written by myself
'''

class TopicQuestionsTest(TestCase):
    # A topic instance that will only be used for testing
    def setUp(self):
        Topic.objects.create(name='QMConnect+', description='University topic.')

    """
    It tests if Django returns the (success) status code
    200 for an existing Topic.
    """
    def test_topic_questions_view_status_code_200(self):
        url = reverse('qa:topic_questions', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    """
    It tests if Django returns the (page not found)
    status code 400 for a Topic that is not in the db.
    """
    def test_topic_questions_view_status_code_404(self):
        url = reverse('qa:topic_questions', kwargs={'pk': 101})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    """
    It tests if Django is using the correct view function
    to render the topics.
    """
    def test_topic_questions_url_resolves_topic_questions_view(self):
        view = resolve('/topics/1/')
        self.assertEquals(view.func.view_class, QuestionsView)

    """
    It checks if the view has the navigation links such as
    going back to the homepage or adding a new questions
    """
    def test_topic_questions_view_has_navigations_links(self):
        topic_questions_url = reverse('qa:topic_questions', kwargs={'pk': 1})
        response = self.client.get(topic_questions_url)
        homepage_url = reverse('qa:latest')
        new_question_url = reverse('qa:new_question', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_question_url))
