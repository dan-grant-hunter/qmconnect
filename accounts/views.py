from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, ProfileForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Profile, Module, Interest

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
