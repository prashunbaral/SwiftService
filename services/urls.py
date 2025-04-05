from django.urls import path
from .views import (
    CategoryListView, CategoryDetailView,
    SkillListView, SkillDetailView,
    ServiceListView, ServiceDetailView, ServiceCreateView, 
    ServiceUpdateView, ServiceDeleteView,create_service_form
)

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),

    # Skill URLs
    path('categories/<int:category_id>/skills/', SkillListView.as_view(), name='skill_list'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill_detail'),

    # Service URLs
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/create/', ServiceCreateView.as_view(), name='create_service'),
    path('services/create/form/', create_service_form, name='create_service_form'),

    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='update_service'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='delete_service'),
]