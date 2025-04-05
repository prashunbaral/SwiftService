from django import forms
from .models import Service, Category, Skill

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['skill','title', 'description', 'price', 'is_available']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'description']





        