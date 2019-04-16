from django.urls import path
from . import views as qa_views
from accounts import views as accounts_views

app_name = 'qa'
urlpatterns = [
    path('', qa_views.latest, name='latest'),
    path('topics/', qa_views.TopicsView.as_view(), name='home'),
    path('topics/<int:pk>/', qa_views.QuestionsView.as_view(), name = 'topic_questions'),
    path('topics/<int:pk>/new/', qa_views.new_question, name = 'new_question'),
    path('topics/<int:pk>/questions/<int:question_pk>/', qa_views.AnswersView.as_view(), name = 'question_answers'),
    path('topics/<int:pk>/questions/<int:question_pk>/reply/', qa_views.answer_question, name = 'answer_question'),
    path('topics/<int:pk>/questions/<int:question_pk>/answers/<int:answer_pk>/edit/', qa_views.AnswerUpdateView.as_view(), name = 'modify_answer'),
    path('network/', accounts_views.network, name='network'),
    path('profile/<int:pk>/', accounts_views.profile, name='profile'),
    path('messages/', accounts_views.messages, name='messages'),
    path('messages/<int:pk>/send_message/', accounts_views.send_message, name='send_message'),
    path('buddy/', accounts_views.studybuddy, name='studybuddy'),
    path('conversation/<int:pk>/', accounts_views.conversation, name='conversation'),
    path('conversation/new', accounts_views.new_conversation, name='new_conversation'),
]
