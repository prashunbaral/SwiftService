from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, CategoryViewSet, ServiceViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')

# Auth URLs need to be defined separately since they don't follow standard viewset patterns
auth_urls = [
    path('auth/register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    path('auth/logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
]

urlpatterns = auth_urls + [
    path('', include(router.urls)),
] 