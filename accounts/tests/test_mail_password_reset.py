from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

'''
Code written by myself following the tutorial: https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/
'''

class MailPasswordResetTests(TestCase):
    # dummy data that will be used for the tests
    def setUp(self):
        User.objects.create_user(username='cp', email = 'cp@gmail.com', password = 'superStrongPw!2-10')
        self.response = self.client.post(reverse('password_reset'), {'email': 'cp@gmail.com'})
        self.email = mail.outbox[0]

    '''
    Test the subject of the email.
    '''
    def test_email_subject(self):
        self.assertEqual('QMConnect+ - Reset your password', self.email.subject)

    """
    It tests the body of the email sent by the system.
    """
    def test_password_reset_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        passw_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(passw_reset_token_url, self.email.body)
        self.assertIn('cp', self.email.body)
        self.assertIn('cp@gmail.com', self.email.body)

    """
    Testing if the receiver of the email is the
    intended one.
    """
    def test_receiver_email(self):
        self.assertEqual(['cp@gmail.com'], self.email.to)
