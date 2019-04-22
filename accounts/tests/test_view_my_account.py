from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from accounts.views import AccountUpdateView
from accounts.models import Profile, Module, Interest

'''
Code written by myself following the tutorial: https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/
'''

class MyAccountTestCase(TestCase):
    def setUp(self):
        self.username = 'Catalin',
        self.password = 'mypassw159'
        self.module = Module.objects.create(name='Web Programming')
        self.interest = Interest.objects.create(name='Python')
        self.user = User.objects.create_user(username=self.username, email="cp@gmail.com", password=self.password)
        self.profile = Profile.objects.create(user=self.user, dob='1990-08-08', image='', universityYear='1', subject='BSc Computer Science')
        self.profile.module.add(self.module)
        self.profile.interest.add(self.interest)
        self.url = reverse('account_update')

class MyAccountTests(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    '''
    Check the status code of the response.
    '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    '''
    Check if the url executes the associated
    view function - AccountUpdateView.
    '''
    def test_url_resolves_proper_view(self):
        view = resolve('/settings/account')
        self.assertEquals(view.func.view_class, AccountUpdateView)

    '''
    Tests that the response contains the
    csrf middleware token.
    '''
    def test_response_has_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    '''
    Check if the form is an instance of the
    ModelForm.
    '''
    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, ModelForm)

    '''
    Ensures that the form contains all the necessary inputs:
        - image
        - university year
        - module
        - interest
    '''
    def test_form_contains_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, '<select', 3)
        self.assertContains(self.response, 'type="file"', 1)

class MyAccountRequiresLoginTests(TestCase):
    '''
    Ensures that the my account section can only be accessed
    if the user is logged in.
    '''
    def test_redirection(self):
        url = reverse('account_update')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

class MyAccountSuccessfulUpdate(MyAccountTestCase):
    def setUp(self):
        # log the user in
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        # update the information to other modules and interests
        module = Module.objects.create(name='Big Data Processing')
        interest = Interest.objects.create(name='Java Programming')
        # make a POST request with the new data
        self.response = self.client.post(self.url, {
            'image': '',
            'universityYear': '1',
            'module': module.pk,
            'interest': interest.pk
        })

    '''
    Tests if the updated details are in the response:
        - module
        - interest
        - university year
    '''
    def test_information_updated(self):
        self.assertContains(self.response, self.module)
        self.assertContains(self.response, self.interest)
        self.assertContains(self.response, '3rd year')

class MyAccountUnsuccessfulUpdate(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {
            'first_name': 'longstring' * 100
        })

    '''
    If invalid form submission,
    return to the same page.
    '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    '''
    Tests that the form displays the errors.
    '''
    def test_form_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)
