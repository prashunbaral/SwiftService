from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserProfile, ServiceProvider

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_service_provider', 'phone_number')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_service_provider', 'phone_number')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture')



class ServiceProviderForm(forms.ModelForm):
    class meta:
        model = ServiceProvider
        fields = ('skills', 'experience', 'service_area')

