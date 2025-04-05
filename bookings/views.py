from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Booking, BookingReview
from .serializers import BookingSerializer, BookingReviewSerializer

# Booking Views
class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return bookings for the logged-in user
        return Booking.objects.filter(customer=self.request.user)


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow access to the logged-in user's bookings
        return Booking.objects.filter(customer=self.request.user)


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the customer to the logged-in user
        serializer.save(customer=self.request.user)


class BookingCancelView(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow the logged-in user to cancel their own bookings
        return Booking.objects.filter(customer=self.request.user)

    def perform_update(self, serializer):
        # Set the status to 'cancelled'
        if serializer.instance.status not in ['pending', 'confirmed']:
            raise PermissionDenied("You can only cancel pending or confirmed bookings.")
        serializer.save(status='cancelled')


# Booking Review Views
class BookingReviewCreateView(generics.CreateAPIView):
    serializer_class = BookingReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.validated_data['booking']
        # Ensure the booking belongs to the logged-in user and is completed
        if booking.customer != self.request.user or booking.status != 'completed':
            raise PermissionDenied("You can only review completed bookings.")
        serializer.save()


class BookingReviewDetailView(generics.RetrieveAPIView):
    serializer_class = BookingReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow access to reviews for the logged-in user's bookings
        return BookingReview.objects.filter(booking__customer=self.request.user)