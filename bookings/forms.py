from django import forms
from .models import Booking, BookingReview

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['Service', 'booking_date', 'notes']
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class BookingReviewForm(forms.ModelForm):
    class Meta:
        model = BookingReview
        fields = ['rating', 'comments']