from django.test import TestCase
from accounts.forms import RegisterForm

'''
Code written by myself
'''

class RegisterFormTest(TestCase):
    def test_form_has_field(self):
        form = RegisterForm()
        expected = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
