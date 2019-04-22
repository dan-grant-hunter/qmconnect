from django.urls import reverse, resolve
from django.test import TestCase
from qa.models import Topic, Question, Answer
from qa.views import TopicsView
from django.utils import timezone
from accounts.views import profile
from django.contrib.auth.models import User

'''
Code written by myself
'''

# This class tests the "profile" webpage when the user is logged in
class ProfileTests(TestCase):
    """
    Get the URL to the profile page
    Log the user in
    The webpage requires a user to be logged in
    """
    def setUp(self):
        # create a new user
        self.user = User.objects.create_user(username='catalin', email='pit@gmail.com', password='tiptiP161!')
        # get the url for this view function
        # pass the pk to the profile function
        # reverse returns the url
        url = reverse('qa:profile', kwargs={'pk': self.user.pk})
        # log the user in
        self.client.login(username='catalin', password='tiptiP161!')
        # get the response from the url
        self.response = self.client.get(url)

    """
    Tests that Django returns the (success) status code
    200 for the "Profile" webpage
    """
    def test_profile_status_code_200(self):
        self.assertEquals(self.response.status_code, 200)

    """
    Test if the right view function is used for the request
    The profile webpage should return the profile view function
    """
    def test_profile_returns_right_view_function(self):
        # resolve returns the following information:
        # - func=accounts.views.profile,
        # - args=(),
        # - kwargs={'pk': 1},
        # - url_name=profile,
        # - app_names=['qa'],
        # - namespaces=['qa'])
        view = resolve("/profile/1/")
        self.assertEquals(view.func, profile)

# This class tests the "profile" webpage when there is an anonymous user
class AnonymousUserProfilePage(TestCase):
    def setUp(self):
        # create a new user
        self.user = User.objects.create_user(username='catalin', email='pit@gmail.com', password='tiptiP161!')
        # get the url for this view function
        # pass the pk to the profile function
        # reverse returns the url
        self.url = reverse('qa:profile', kwargs={'pk': self.user.pk})
        # get the response from the url
        self.response = self.client.get(self.url)

    """
    Tests that Django returns the status code 302,
    which represents redirection, when an anonymous user
    tries to access the profile webpage
    """
    def test_profile_status_code_302(self):
        self.assertEquals(self.response.status_code, 302)

    """
    Tests that the anonymous user is redirected to the login page
    """
    def test_redirect_to_login_page(self):
        login_url = reverse('login')
        # use string formatting '{}'.format()
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
