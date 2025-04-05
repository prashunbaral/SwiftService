from django.contrib import admin
from .models import Booking, BookingReview

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    def get_service(self, obj):
        return obj.Service.title
    
    get_service.short_description = 'Service'
    list_display = ('id', 'get_service', 'customer', 'booking_date', 'status', 'created_at')

@admin.register(BookingReview)
class BookingReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('booking__service__title', 'booking__customer__username')