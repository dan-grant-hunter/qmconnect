from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from .forms import NewQuestionForm, PostForm
from .models import Topic, Question, Answer
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from accounts.models import Interest, Profile
from accounts.models import Interest, Conversation, Message
from django.http import JsonResponse

class TopicsView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        '''
        Retrieve the most popular topic
        '''
        # get the question with the highest number of questions
        mostQuestions = context['object_list'][0].questions_count()

        # get the name of the topic with the highest number of questions
        mostQuestionsTopic = context['object_list'][0]

        '''
        Retrieve the most popular question
        '''
        # the number of answers a question has
        mostAnswers = 0
        # the name of the question with the most answers
        mostAnswersQuestion = ''

        # for each topic in the object list from the context
        for topic in context['object_list']:
            # for each question in the list of questions from each topic
            for question in Question.objects.filter(topic = topic):
                if question.answers.count() > mostAnswers:
                    mostAnswers = question.answers.count()
                    mostAnswersQuestion = question

            if topic.questions_count() > mostQuestions:
                mostQuestions = topic.questions_count()
                mostQuestionsTopic = topic

        # add the new information to the context
        context['mostQuestions'] = mostQuestions
        context['mostQuestionsTopic'] = mostQuestionsTopic
        context['mostAnswers'] = mostAnswers
        context['mostAnswersQuestion'] = mostAnswersQuestion

        return context

class QuestionsView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'questions.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, pk = self.kwargs.get('pk'))
        queryset = self.topic.questions.order_by('-last_updated').annotate(replies=Count('answers') - 1)
        return queryset

class AnswersView(ListView):
    model = Answer
    context_object_name = 'answers'
    template_name = 'question_answers.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        session_key = 'viewed_question_{}'.format(self.question.pk)
        if not self.request.session.get(session_key, False):
            self.question.views += 1
            self.question.save()
            self.request.session[session_key] = True

        kwargs['question'] = self.question
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.question = get_object_or_404(Question, topic__pk = self.kwargs.get('pk'), pk = self.kwargs.get('question_pk'))
        queryset = self.question.answers.order_by('created_at')
        return queryset

@login_required
def new_question(request, pk):
    # retrieve the topic of the question (e.g. Enrollment)
    topic = get_object_or_404(Topic, pk=pk)

    if request.method == 'POST':
        # instantiate the form with the POST data received from the request
        form = NewQuestionForm(request.POST)
        # store the user currently logged in/that made the request
        user = request.user

        # check if the form is valid,
        # if so, save the data to the db
        if form.is_valid():
            # do not commit the save to the database
            # as the topic and starter needs to be associated with the question
            question = form.save(commit=False)
            question.topic = topic
            question.starter = user
            # once the topic and the starter are associated with the question
            # save it to the database
            question.save()

            # create a new answer with the description entered by the user
            # and with the question and the user who answered
            answer = Answer.objects.create(
                message = form.cleaned_data.get('description'),
                question = question,
                created_by = user
            )

            return redirect('qa:question_answers', pk = pk, question_pk = question.pk)

    else:
        form = NewQuestionForm()

    return render(request, 'new_question.html', {'topic': topic, 'form': form})

@login_required
def answer_question(request, pk, question_pk):
    # retrieve the question for which an answer is posted
    question = get_object_or_404(Question, topic__pk = pk, pk = question_pk)

    # proceed further only if the request is a POST request
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.created_by = request.user
            answer.save()

            question.last_updated = timezone.now()
            question.save()

            question_url = reverse('qa:question_answers', kwargs = {'pk': pk, 'question_pk': question_pk})
            question_answer_url = '{url}?page={page}#{id}'.format(
                url = question_url,
                id = answer.pk,
                page = question.get_page_count()
            )

    # create a dictionary with the new message
    data = {}
    data['message'] = answer.message
    data['created_at'] = answer.created_at
    data['created_by'] = answer.created_by.username
    data['image'] = str(answer.created_by.profile.image)

    return JsonResponse(data, safe=False)

@method_decorator(login_required, name='dispatch')
class AnswerUpdateView(UpdateView):
    model = Answer
    fields = ('message', )
    template_name = 'modify_answer.html'
    '''
    identifies the name of the keyword arg used to
    retrieve the Answer obj
    '''
    pk_url_kwarg = 'answer_pk'
    '''
    allows to navigate through the Answer object
    such as answer.question.topic.pk
    '''
    context_object_name = 'answer'

    def get_queryset(self):
        queryset = super().get_queryset()
        '''
        ensures only the user that created the answer
        can edit it
        '''
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.updated_by = self.request.user
        answer.updated_at = timezone.now()
        answer.save()

        return redirect('qa:question_answers', pk = answer.question.topic.pk, question_pk = answer.question.pk)

def latest(request):
    # retrieve the latest ten answers and questions
    # order them in descending order by the time they were posted/updated
    answers = Answer.objects.order_by('-created_at')[:10]
    questions = Question.objects.order_by('-last_updated')[:10]
    return render(request, 'latest.html', {'answers': answers, 'questions': questions})
