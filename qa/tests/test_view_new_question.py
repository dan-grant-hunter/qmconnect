from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from .models import Topic, Question, Answer
from .views import new_question
from .forms import NewQuestionForm

class NewQuestionsTests(TestCase):
    """
    It creates a Topic instance that will be used
    during the tests.
    """
    def setUp(self):
        Topic.objects.create(name='QMConnect+', description='A platform for students from students.')
        User.objects.create_user(username='pit', email='pit@gmail.com', password='tiptiP161!')
        self.client.login(username='pit', password='tiptiP161!')

    """
    It checks if a 404 error is triggered when the
    Topic does not exist.
    """
    def test_new_question_view_status_code_404(self):
        url = reverse('new_question', kwargs={'pk': 101})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    """
    It check if the request to the view is returning 200
    (if it's successful)
    """
    def test_new_question_view_status_code_202(self):
        url = reverse('new_question', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    """
    Checking if the right view is used for the request.
    """
    def test_new_question_url_returns_new_question_view(self):
        view = resolve('/topics/1/new/')
        self.assertEquals(view.func, new_question)

    """
    Make sure that navigation back to the list of questions
    is available.
    """
    def test_new_question_view_if_links_back_to_topic_questions_view(self):
        new_question_url = reverse('new_question', kwargs={'pk': 1})
        topic_questions_url = reverse('QuestionsView', kwargs={'pk': 1})
        response = self.client.get(new_question_url)
        self.assertContains(response, 'href="{0}"'.format(QuestionsView_url))

    """
    It ensures that the CSRF token is included in the HTML.
    """
    def test_csrf_middleware_token(self):
        url = reverse('new_question', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    """
    It makes sure that the view creates Question and Answer instances.
    """
    def test_new_question_creates_instances(self):
        url = reverse('new_question', kwargs={'pk': 1})
        info = {
            'subject': 'QMConnect+123',
            'description': 'Connecting people.123'
        }
        self.client.post(url, info)
        self.assertTrue(Question.objects.exists())
        self.assertTrue(Answer.objects.exists())

    """
    Test the form with empty data. It should display
    the form again with validation errors.
    """
    def test_new_question_no_data(self):
        url = reverse('new_question', kwargs={'pk': 1})
        response = self.client.get(url, {})
        self.assertEquals(response.status_code, 200)

    """
    Test the behaviour of the form with empty data.
    """
    def test_new_question_with_empty_fields(self):
        url = reverse('new_question', kwargs={'pk': 1})
        info = {
            'subject': '',
            'description': ''
        }
        response = self.client.post(url, info)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Question.objects.exists())
        self.assertFalse(Answer.objects.exists())

    """
    It tests if a new form is a NewQuestionForm instance.
    """
    def test_its_a_newquestionform_instance(self):
        url = reverse('new_question', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewQuestionForm)

    """
    Testing if the form displays the proper errors
    when the data is invalid/empty.
    It should display the form again with the
    validation errors.
    """
    def test_new_question_form_validations(self):
        url = reverse('new_question', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

'''
It checks if the 'new question' view requires the user
to be authenticated before posting a new question.
'''
class NewQuestionRequiresLoginTests(TestCase):
    def setUp(self):
        Topic.objects.create(name='QMConnect+', description='A platform for students from students.')
        self.url = reverse('new_question', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    '''
    It should redirect the user to the login page
    if not authenticated.
    '''
    def test_redirect(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
