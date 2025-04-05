from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class CustomUser(AbstractUser):
    is_service_provider = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class ServiceProvider(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    skills = models.ManyToManyField('services.Skill')
    experience = models.IntegerField(default=0)
    service_area = models.CharField(max_length=100, blank= True)

    def __str__(self):
        return f"{self.user.username} - Service Provider"