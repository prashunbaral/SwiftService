from django.urls import path
from .views import (
    BookingListView, BookingDetailView, BookingCreateView, BookingCancelView,
    BookingReviewCreateView, BookingReviewDetailView
)

urlpatterns = [
    # Booking URLs
    path('', BookingListView.as_view(), name='booking_list'),  # List all bookings for the logged-in user
    path('<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),  # Retrieve a specific booking
    path('create/', BookingCreateView.as_view(), name='create_booking'),  # Create a new booking
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='cancel_booking'),  # Cancel a booking

    # Booking Review URLs
    path('<int:pk>/review/', BookingReviewCreateView.as_view(), name='create_review'),  # Create a review for a booking
    path('review/<int:pk>/', BookingReviewDetailView.as_view(), name='review_detail'),  # Retrieve a specific review
]