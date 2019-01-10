from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.models import User
from ..views import register
from ..forms import RegisterForm

# Create your tests here.
class RegisterTests(TestCase):
    """
    It tests if a request to the register page
    returns the success status code - 200.
    """
    def test_register_request_status_code(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    """
    Testing if the url is returning the appropriate
    view function.
    """
    def test_register_url_returns_correct_register_view(self):
        view = resolve('/register/')
        self.assertEquals(view.func, register)

    """
    It tests if there is a form in the response.
    """
    def test_response_contains_form(self):
        url = reverse('register')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, RegisterForm)

    """
    Testing if the response also contains a CSRF token.
    """
    def test_response_contains_csrf_token(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    """
    Ensuring that the form only includes five fields such as
    csrf, user name, email address, password1 and password2.
    """
    def test_form_fields(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertContains(response, '<input', 5)
        self.assertContains(response, 'type="text"', 1)
        self.assertContains(response, 'type="email"', 1)
        self.assertContains(response, 'type="password"', 2)

class RegisterSuccessfullyTests(TestCase):
    # Default class that will be used for the tests in this class
    def setUp(self):
        url = reverse('register')
        data = {
            'username': 'cp',
            'email': 'cp@mail.com',
            'password1': 'thirdyearproject',
            'password2': 'thirdyearproject'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    """
    Tests if the user is redirected to the home page
    after a valid form submission.
    """
    def test_valid_submission_redirect(self):
        self.assertRedirects(self.response, self.home_url)

    """
    Testing if the user is created successfully.
    """
    def test_user_creation_successfully(self):
        self.assertTrue(User.objects.exists())

    """
    It checks if the response has a 'user' to its context
    after a successful registration.
    """
    def test_successful_registration_user_auth(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class UnsuccessfulRegistrationTests(TestCase):
    def setUp(self):
        url = reverse('register')
        # empty data submitted
        self.response = self.client.post(url, {})

    """
    Checking if the user is returned to the same page
    (register) after an invalid submission.
    """
    def test_status_code_register(self):
        self.assertEquals(self.response.status_code, 200)

    """
    It tests if the registration of the user was
    unsuccessfully.
    """
    def test_user_creation_unsuccessfully(self):
        self.assertFalse(User.objects.exists())

    """
    It checks if there are any form errors.
    """
    def test_if_form_has_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
