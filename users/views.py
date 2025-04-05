from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserCreationForm, UserProfileForm, ServiceProviderForm
from .models import CustomUser, UserProfile, ServiceProvider
# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'users/profile.html', {'form': form})

@login_required
def service_provider_profile(request):
    service_provider, created = ServiceProvider.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, instance=service_provider)
        if form.is_valid():
            form.save()
            return redirect('service_provider_profile')
    else:
        form = ServiceProviderForm(instance=service_provider)
    return render(request, 'users/service_provider_profile.html', {'form': form})

    #checking
