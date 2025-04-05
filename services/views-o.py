from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service, Category, Skill
from .forms import ServiceForm, CategoryForm, SkillForm

# Create your views here.

def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'services/service_list.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'services/service_detail.html', {'service': service})

@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(request, 'Service created successfully')
            return redirect('service_detail', service_id=service.id)
    else:
        form = ServiceForm()
    return render(request, 'services/create_service.html', {'form': form})

@login_required
def update_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, provider=request.user)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully')
            return redirect('service_detail', service_id=service.id)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, provider=request.user)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully')
        return redirect('service_list')
    return render(request, 'services/service_confirm_delete.html', {'service': service})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'services/category_list.html', {'categories': categories})

def skill_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    skills = Skill.objects.filter(category=category)
    return render(request, 'services/skill_list.html', {'skills': skills})