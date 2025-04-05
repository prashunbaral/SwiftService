from rest_framework import serializers
from .models import Category, Skill, Service

class CategorySerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'skills']


class SkillSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    services = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'description', 'services']


class ServiceSerializer(serializers.ModelSerializer):
    provider = serializers.StringRelatedField(read_only=True)
    skill = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'provider', 'skill', 'title', 'description', 
            'price', 'is_available', 'created_at', 'updated_at'
        ]