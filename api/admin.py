from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Service, Booking

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'provider', 'price', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description', 'provider__email')
    ordering = ('-created_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'customer', 'date', 'time', 'status', 'total_price')
    list_filter = ('status', 'date')
    search_fields = ('service__title', 'customer__email', 'location')
    ordering = ('-created_at',) 