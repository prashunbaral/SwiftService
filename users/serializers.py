from rest_framework import serializers
from .models import CustomUser, UserProfile, ServiceProvider
from services.models import Skill

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_service_provider', 'phone_number']


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture']


class ServiceProviderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = ServiceProvider
        fields = ['id', 'user', 'skills', 'experience', 'service_area']