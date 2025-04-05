from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    path('create/', views.create_service, name='create_service'),
    path('<int:service_id>/update/', views.update_service, name='update_service'),
    path('<int:service_id>/delete/', views.delete_service, name='delete_service'), 
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.skill_list, name='skill_list'),
]