from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:service_id>/', views.create_booking, name='create_booking'),
    path('', views.booking_list, name='booking_list'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('<int:booking_id>/review/', views.create_review, name='create_review'),
]
