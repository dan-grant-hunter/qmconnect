from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from ..views import AccountUpdateView

class MyAccountTestCase(TestCase):
    def setUp(self):
        self.username = 'Catalin',
        self.password = 'mypassw159'
        self.user = User.objects.create_user(username=self.username, email="cp@gmail.com", password=self.password)
        self.url = reverse('my_account')

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
        url = resolve('/settings/myaccount/')
        self.assertEquals(view.func.view_class, AccountUpdateView)

    '''
    Ensure that the response contains the
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
    Ensures that the form contains all the four inputs:
        - first name,
        - last name,
        - email
        - csrf token
    '''
    def test_form_contains_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="email"', 1)

class MyAccountRequiresLoginTests(TestCase):
    '''
    Ensures that the my account section can only be accessed
    if the user is logged in.
    '''
    def test_redirection(self):
        url = reverse('my_account')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

class MyAccountSuccessfulUpdate(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {
            'first_name': 'Catalin',
            'last_name': 'Pit',
            'email': 'cpit@gmail.com',
        })

    '''
    It makes sure that a valid from submission redirects the user.
    '''
    def test_successful_update_redirect(self):
        self.assertRedirects(self.response, self.url)

    '''
    Tests if the user instance is refreshed from database
    to retrieve the updated data.
    '''
    def test_information_updated(self):
        self.user.refresh_from_db()
        self.assertEquals('Catalin', self.user.first_name)
        self.assertEquals('Pit', self.user.last_name)
        self.assertEquals('cp@gmail.com', self.user.email)

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
    It tests if the form displays the errors.
    '''
    def test_form_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)
