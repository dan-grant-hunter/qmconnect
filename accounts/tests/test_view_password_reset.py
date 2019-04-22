from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

'''
Code written by myself following the tutorial: https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/
'''

class PasswordResetTests(TestCase):
    # The function will be used in all tests
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    """
    It tests the status code returned by a request
    made to the password reset page.
    """
    def test_pass_reset_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    """
    It tests if the app returns the proper view
    for the request.
    """
    def test_reset_returns_correct_view(self):
        url = resolve('/reset/')
        self.assertEquals(url.func.view_class, auth_views.PasswordResetView)

    """
    Checking if the response contains a CSRF token.
    """
    def test_response_has_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    """
    It checks if the page contains a form.
    """
    def test_has_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    """
    Tests if the form has the 2 inputs needed:
    the CSRF token and the email.
    """
    def test_form_has_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)

class PasswordResetSuccessfullyTests(TestCase):
    def setUp(self):
        email = 'cp@gmail.com'
        User.objects.create_user(username = 'Catalin', email = email, password='testing1234')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    """
    It tests if a valid form submission redirects the user
    the view called 'password_reset_done' view.
    """
    def test_valid_form_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    """
    Testing if it sends a password reset link to email.
    """
    def test_send_password_reset_email(self):
        self.assertEquals(1, len(mail.outbox))

class PasswordResetUnsuccessfullyTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'user@mail.com'})

    """
    Invalid emails should also redirect the user to the
    'password_reset_done' view.
    """
    def test_invalid_form_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    """
    Ensures that a reset password link will not
    be sent if the email is invalid.
    """
    def test_no_reset_password_link_sent(self):
        self.assertEquals(0, len(mail.outbox))

class PasswordResetDoneTests(TestCase):
    def setup(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    '''
    Checks if returns the correct view function.
    '''
    def test_view_function(self):
        view = resolve('/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)

class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username = 'Catalin', email = 'cp@gmail.com', password='testing1234')

        '''
        It creates a valid password reset token
        Based on how Django creates the token internally.
        '''
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    '''
    Ensures that the correct view function is
    triggered.
    '''
    def test_view_function(self):
        view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

    '''
    It tests that the response contains a csrf token.
    '''
    def test_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    '''
    It checks if the form has two inputs:
    The csrf token and the two password fields.
    '''
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)

class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username = 'Catalin', email = "cp@email.com", password='testing1234')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        '''
        Reset the password to invalidate the token.
        '''
        user.set_password('safa241')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'Invalid link, try again or ignore the message')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))

class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)
