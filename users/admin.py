from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, ServiceProvider
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_service_provider', 'phone_number']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_service_provider', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_service_provider', 'phone_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(ServiceProvider)