from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login
from .forms import RegisterForm, ProfileForm, MessageForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Profile, Module, Interest, Message, Conversation
from django.utils import timezone
from .filters import ProfileFilter
from qa.models import Question
from collections import *

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
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'account_update.html'
    success_url = reverse_lazy('account_update')

    def get_object(self):
        return self.request.user

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
            # save the message to the database
            message.save()

            return redirect('qa:messages', pk = pk)
    else:
        form = MessageForm()

    return render(request, 'new_message.html', {'form': form})

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
def messages(request, pk):
    # get the user requested in the url
    user = get_object_or_404(User, pk=pk)

    # return the conversations where the user has participated
    conversations = Message.objects.filter(conversation__members=user)

    return render(request, 'messages.html', {'conversations': conversations})


@login_required
def find_studybuddy(request):
    # retrieve all the users except the admin
    users = User.objects.all().exclude(username='admin')

    # the logged in user that makes the request
    currentUser = Profile.objects.get(user=request.user)

    '''
    retrieve all the users that:
        have common interests and modules with currentUser
        are in the same year with currentUser
    '''
    common_interests = Profile.objects.filter(interest__in=currentUser.interest.all()).exclude(id=currentUser.id)
    common_modules = Profile.objects.filter(module__in=currentUser.module.all()).exclude(id=currentUser.id)
    same_year = Profile.objects.filter(universityYear=currentUser.universityYear)

    # intersect the three querysets
    # stores all the
    related_users = common_interests.intersection(common_modules, same_year)

    test = Counter(related_users).most_common(10)
    test1 = [user for user,count in test]

    print(related_users)
    print(test, test1)

    return HttpResponse(related_users[0])
