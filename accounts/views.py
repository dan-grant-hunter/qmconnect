from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, ProfileForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        profileForm = ProfileForm(request.POST)
        if form.is_valid() and profileForm.is_valid():
            user = form.save()
            profile = profileForm.save(commit=False)

            profile.user = user
            profile.save()

            print(request.POST)
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
