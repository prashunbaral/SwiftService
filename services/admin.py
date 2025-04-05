from django.contrib import admin
from .models import Service, Category, Skill
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'skill', 'price', 'is_available')
    list_filter = ('is_available', 'skill__category')
    search_fields = ('title', 'description', 'provider__username', 'skill__name')