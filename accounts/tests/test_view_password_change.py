from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

'''
Code written by myself following the tutorial: https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/
'''

class PasswordUpdateTests(TestCase):
    def setUp(self):
        username = 'Catalin'
        password = 'Pit'
        User.objects.create_user(username=username, email='cp@gmail.com', password=password)
        url = reverse('password_update')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)

    '''
    Tests the status code of the response.
    '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    '''
    Ensures that the url triggers the correct view.
    '''
    def test_url_resolves_correct_view(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    '''
    Checks that the response contains the
    csrf middleware token.
    '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    '''
    Checks that the form is an instance of
    PasswordChangeForm.
    '''
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    '''
    Checks if the view has the four inputs:
        - the old password
        - the new password
        - the new password confirmed
        - the csrf token
    '''
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)


class PasswordChangeRequiresLoginTests(TestCase):
    '''
    Checks that changing your password requires
    you to be logged in.
    '''
    def test_redirection(self):
        url = reverse('password_update')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    '''
    Base test case for form processing
    accepts a `data` dict to POST to the view.
    '''
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='Catalin', email='cp@gmail.com', password='old_password')
        self.url = reverse('password_update')
        self.client.login(username='Catalin', password='old_password')
        self.response = self.client.post(self.url, data)


class PasswordChangeSuccessfulTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    '''
    If valid form submission, redirect the user.
    '''
    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    '''
    Get the new password hash updated by refreshing
    the user instance from the database.
    '''
    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    '''
    Create a new request to an arbitrary page.
    The resulting response should now have an `user` to its context, after a successful sign up.
    '''
    def test_user_authentication(self):
        response = self.client.get(reverse('qa:latest'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class PasswordChangeUnsuccessfulTests(PasswordChangeTestCase):
    '''
    Invalid form submission should return to the same page.
    '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    '''
    The form should display the errors when appropriate.
    '''
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    '''
    The user instance should be refreshed from the database
    in order to have the updated data.
    '''
    def test_password_not_updated(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
