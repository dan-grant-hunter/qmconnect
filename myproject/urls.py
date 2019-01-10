"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
'\d' - matches an integer of arbitrary size;
       it will be used to retrieve the topic from the db.

'(?P<pk>\d+)' - capture the value into a keyword argument called pk.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from accounts import views as accs_views

urlpatterns = [
    path('', include('qa.urls')),
    path('register/', accs_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('settings/account', accs_views.AccountUpdateView.as_view(), name = 'account_update'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name = 'password_reset.html',
            email_template_name = 'password_reset_email.html',
            subject_template_name = 'password_reset_subject.txt'
        ),
        name = 'password_reset'
    ),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'),
        name = 'password_reset_done'
    ),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'),
        name = 'password_reset_confirm'
    ),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'),
        name = 'password_reset_complete'
    ),
    path('profile/password/', auth_views.PasswordChangeView.as_view(template_name='password_update.html'),
         name = 'password_update'),
    path('profile/password/successfull', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name = 'password_change_done'),
    path('admin/', admin.site.urls),
]

#re_path(r'^topics/(?P<pk>\d+)/$', qa_views.QuestionsView.as_view(), name = 'topic_questions'),
#re_path(r'^topics/(?P<pk>\d+)/new/$', qa_views.new_question, name = 'new_question'),
#re_path(r'^topics/(?P<pk>\d+)/questions/(?P<question_pk>\d+)/$', qa_views.AnswersView.as_view(), name = 'question_answers'),
#re_path(r'^topics/(?P<pk>\d+)/questions/(?P<question_pk>\d+)/reply/$', qa_views.answer_question, name = 'answer_question'),

# path('', qa_views.TopicsView.as_view(), name='home'),
# path('topics/<int:pk>/', qa_views.QuestionsView.as_view(), name = 'topic_questions'),
# path('topics/<int:pk>/new/', qa_views.new_question, name = 'new_question'),
# path('topics/<int:pk>/questions/<int:question_pk>/', qa_views.AnswersView.as_view(), name = 'question_answers'),
# path('topics/<int:pk>/questions/<int:question_pk>/reply/', qa_views.answer_question, name = 'answer_question'),
# path('topics/<int:pk>/questions/<int:question_pk>/answers/<int:answer_pk>/edit/', qa_views.AnswerUpdateView.as_view(), name = 'modify_answer'),
