from django.urls import reverse, resolve
from django.test import TestCase
from qa.models import Topic, Question, Answer
from accounts.models import Profile, Module, Interest
from qa.views import TopicsView
from accounts.views import studybuddy
from django.utils import timezone
from django.contrib.auth.models import User

class FindBuddyTests(TestCase):
    """
    Get the URL to the buddy webpage
    Store the response in self.response
    The webpage requires a user to be logged in
    """
    def setUp(self):
        # create a new user
        self.user = User.objects.create_user(username='catalin', email='pit@gmail.com', password='tiptiP161!')
        # create a new module to add it to the profile
        self.module = Module.objects.create(name='Web Programming')
        # create a new interest to add it to the profile
        self.interest = Interest.objects.create(name='Python')
        # create a new profile instance because the studybuddy view function
        # creates a profile instance from request.user
        self.profile = Profile.objects.create(user=self.user, dob='1990-08-08', image='', universityYear='1', subject='BSc Computer Science')
        # add the module and interest to the profile
        self.profile.module.add(self.module)
        self.profile.interest.add(self.interest)
        # log the user in
        self.client.login(username='catalin', password='tiptiP161!')
        # get the url for this view function
        # and the response code
        url = reverse('qa:studybuddy')
        self.response = self.client.get(url)

    """
    It tests if Django returns the (success) status code
    200 for the "Find a buddy" webpage
    """
    def test_studybuddy_status_code_200(self):
        self.assertEquals(self.response.status_code, 200)

    """
    Checking if the right view is used for the request.
    """
    def test_buddy_url_returns_studybuddy_view(self):
        # retrieve the view of this url
        view = resolve('/buddy/')
        self.assertEquals(view.func, studybuddy)

"""
Tests if the buddy webpage requires the user to be
logged in to access it.
"""
class UnauthenticatedFindBuddyTests(TestCase):
    def setUp(self):
        # get the url for this view function
        # and the response code
        self.url = reverse('qa:studybuddy')
        self.response = self.client.get(self.url)

    """
    It should redirect the user to the login page
    if not authenticated.
    """
    def test_redirect(self):
        # get the login url
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
