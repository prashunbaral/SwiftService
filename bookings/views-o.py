from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, BookingReview
from .forms import BookingForm, BookingReviewForm
from services.models import Service

@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Booking created successfully')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'form': form, 'service': service})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully')
        return redirect('booking_detail')
    return render(request, 'bookings/booking_cancel.html', {'booking': booking})

@login_required
def create_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user, status='completed')
    if request.method == 'POST':
        form = BookingReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, 'Review created successfully')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingReviewForm()
    return render(request, 'bookings/review_form.html', {'form': form, 'booking': booking})