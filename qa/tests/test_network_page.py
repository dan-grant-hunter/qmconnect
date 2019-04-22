from django.urls import reverse, resolve
from django.test import TestCase
from qa.models import Topic, Question, Answer
from qa.views import TopicsView
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.views import network
from accounts.filters import ProfileFilter

'''
Code written by myself
'''

# Tests the "Network" webpage with the user being logged in
class NetworkPageTests(TestCase):
    def setUp(self):
        # Create a new user
        self.user = User.objects.create_user(username='catalin', email='pit@gmail.com', password='tiptiP161!')
        # Get the "Network" url
        self.url = reverse('qa:network')
        # Log the user in
        self.client.login(username='catalin', password='tiptiP161!')
        # Retrive the response sent by Django
        self.response = self.client.get(self.url)

    """
    Tests that Django returns the (success) status code
    200 for the "Network" webpage
    """
    def test_network_webpage_response_status_code_200(self):
        # Compare the response status code
        self.assertEquals(self.response.status_code, 200)

    """
    Tests if the right view function is used for the request
    The "Network" webpage should return the network view function
    """
    def test_network_returns_correct_view(self):
        # Get the view function from this url
        view = resolve("/network/")
        # Check that the view functions match
        self.assertEquals(view.func, network)

    """
    Tests that the webpage contains the form for filtering users
    """
    def test_network_webpage_contains_profilefilterForm(self):
        self.assertIn("formFiltering", str(self.response.content))

    """
    Test that the form used in the network webpage is an
    instance of ProfileFilter
    """
    def test_formFiltering_instance(self):
        filterForm = self.response.context.get('user_filter')
        self.assertIsInstance(filterForm, ProfileFilter)

# Tests the "Network" webpage without the user being logged in
class AnonymousUserNetworkPageTests(TestCase):
    def setUp(self):
        # Get the "Network" url
        self.url = reverse('qa:network')
        # Retrive the response sent by Django
        self.response = self.client.get(self.url)

    """
    Tests that Django returns the status code 302,
    which represents redirection, when an anonymous user
    tries to access the "Network" webpage
    """
    def test_network_webpage_response_status_code_302(self):
        # Compare the response status code
        self.assertEquals(self.response.status_code, 302)

    """
    Tests that the anonymous user is redirected to the login page
    """
    def test_redirect_to_login_page(self):
        # Get the login url
        login_url = reverse('login')
        # Check that it redirects to the login page
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
