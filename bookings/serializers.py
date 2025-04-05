from rest_framework import serializers
from .models import Booking, BookingReview

class BookingSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    Service = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'customer', 'Service', 'booking_date', 'status', 
            'created_at', 'updated_at', 'notes'
        ]


class BookingReviewSerializer(serializers.ModelSerializer):
    booking = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BookingReview
        fields = [
            'id', 'booking', 'rating', 'comments', 'created_at'
        ]