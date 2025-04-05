from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Service, Booking

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'profile_picture')
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'phone_number')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'icon', 'created_at')

class ServiceSerializer(serializers.ModelSerializer):
    provider_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ('id', 'title', 'description', 'price', 'category', 'category_name',
                 'provider', 'provider_name', 'image', 'created_at', 'updated_at', 'is_featured')
    
    def get_provider_name(self, obj):
        return f"{obj.provider.first_name} {obj.provider.last_name}".strip() or obj.provider.username
    
    def get_category_name(self, obj):
        return obj.category.name

class BookingSerializer(serializers.ModelSerializer):
    service_title = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ('id', 'service', 'service_title', 'customer', 'customer_name',
                 'date', 'time', 'duration', 'location', 'notes', 'status',
                 'total_price', 'created_at')
        read_only_fields = ('status',)
    
    def get_service_title(self, obj):
        return obj.service.title
    
    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}".strip() or obj.customer.username 