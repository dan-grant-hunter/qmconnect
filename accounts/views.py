from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login
from .forms import RegisterForm, ProfileForm, MessageForm, ConversationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Profile, Module, Interest, Message, Conversation
from django.utils import timezone
from .filters import ProfileFilter
from qa.models import Question
from collections import *
import json
from django.core import serializers

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        profileForm = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profileForm.is_valid():
            user = form.save()

            # do not commit the profile to the database yet
            # the profile needs to be associated with the user and then saved
            # otherwise it results in an error
            profile = profileForm.save(commit=False)

            # associate the profile with the user
            # and save it
            profile.user = user
            profile.save()

            # it needs to check if the user uploaded an image
            # without the if statement,
            # it would result in an error if the user tried to register without uploading an image
            if 'image' in request.FILES:
                profile.image = request.FILES['image']

            # get the modules and interests
            # so they can be added to the profile later
            modules = request.POST.getlist('module')
            interests = request.POST.getlist('interest')

            # iterate over each module and interest
            # and add it to the profile
            for index in modules:
                profile.module.add(Module.objects.get(pk=index))

            for index in interests:
                profile.interest.add(Interest.objects.get(pk=index))

            # log the user in after a successful registration
            login(request, user)
            return redirect('qa:latest')
        else:
            return render(request, 'register.html', {'form': form, 'profileForm': profileForm})
    else:
        form = RegisterForm()
        profileForm = ProfileForm()

        return render(request, 'register.html', {'form': form, 'profileForm': profileForm})

@method_decorator(login_required, name='dispatch')
class AccountUpdateView(UpdateView):
    model = Profile
    fields = ('image', 'universityYear', 'module', 'interest',)
    template_name = 'account_update.html'
    success_url = reverse_lazy('account_update')

    # return the account page of the logged-in user
    def get_object(self):
        return self.request.user.profile

# the function used to send messages
@login_required
def send_message(request, pk):
    # the sender of the message is the user that is currently logged in
    sender = request.user
    # the receiver of the message is the user whose id comes after profile/{pk}/
    receiver = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            # retrieve the text from the form submission
            text = request.POST['text']

            # create a new message
            message = Message(sender = sender.profile, receiver = receiver.profile, text = text, time = timezone.now())
            message.conversation = get_object_or_404(Conversation, pk=request.POST['conversation_id'])

            # save the message to the database
            message.save()

    # create a dictionary with the new message
    # return the new message to the AJAX
    data = {}

    data['sender'] = message.sender.user.username
    data['receiver'] = message.receiver.user.username
    data['text'] = message.text
    data['time'] = message.time
    data['conversation'] = "3"

    # return the new data
    return JsonResponse(data, safe=False)

@login_required
def network(request):
    # get all the profiles
    # exclude the logged in user
    profiles = Profile.objects.all().exclude(user_id=request.user.id)

    # filter the profiles based on the parameters from the GET request made by the user
    user_filter = ProfileFilter(request.GET, queryset=profiles)

    return render(request, 'network.html', {'user_filter': user_filter})

@login_required
def profile(request, pk):
    # get the user requested in the url
    user = get_object_or_404(User, pk=pk)
    # retrieve all the users
    users = User.objects.all()
    # get only the questions asked by the user requested above
    user_questions = Question.objects.filter(starter = user)[:5]

    return render(request, 'profile.html', {
        'user': user,
        'user_questions': user_questions
    })

@login_required
def messages(request):
    # get the user requested in the url
    user = request.user

    # return the conversations where the user has participated
    conversations = Message.objects.filter(conversation__members=user)

    return render(request, 'messages.html', {'conversations': conversations})

'''
This method allows AJAX to retrieve a single conversation
'''
@login_required
def conversation(request, pk):
    # get the user requested in the url
    user = request.user

    # return the conversations where the user has participated
    conversations = Message.objects.filter(conversation__members=user)

    formatted_messages_for_ajax = []

    for message in conversations:
        if message.conversation.pk == pk:
            conversation = str(message)
            formatted_messages_for_ajax.append(conversation)

    return HttpResponse(formatted_messages_for_ajax)


@login_required
def studybuddy(request):
    # retrieve all the users except the admin
    users = User.objects.all().exclude(username='admin')

    # the logged in user that makes the request
    currentUser = Profile.objects.get(user=request.user)

    '''
    retrieve all the users that have common interests and modules with currentUser
    '''
    common_interests = Profile.objects.filter(interest__in=currentUser.interest.all()).exclude(id=currentUser.id)
    common_modules = Profile.objects.filter(module__in=currentUser.module.all()).exclude(id=currentUser.id)

    # count the common interests and modules with the user that makes the request
    # for each common module or/and interests, the value is increment by one
    # e.g. if the user making the request has only 2 common modules with user1, it will return <Profile:user1>,2
    common_interests_counter = Counter(common_interests)
    common_modules_counter = Counter(common_modules)

    # add together the number of common modules and interests
    related_users_counter = (common_modules_counter + common_interests_counter)
    # take only the top 10 students with matching modules and interests
    related_users_counter = related_users_counter.most_common(10)

    # extract the users from the counter
    related_users = [user for user,count in related_users_counter]


    return render(request, 'buddy.html', {'related_users': related_users})
