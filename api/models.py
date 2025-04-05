from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # For storing FontAwesome icon names
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in hours")
    location = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.service.title} - {self.customer.email} - {self.date}" 