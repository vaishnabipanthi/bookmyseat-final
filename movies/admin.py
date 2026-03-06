from django.contrib import admin
from django.db.models import Sum, Count
from .models import Movie, Theater, Seat,Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'cast','description']

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'is_booked']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'movie','theater','booked_at']
    list_filter = ['movie', 'theater', 'booked_at']
    readonly_fields = ['user','seat','movie','theater','booked_at']

def changeList_view(self, request, extra_context=None):
    total_revenue = Booking.objects.count()*200
    popular_Movies=Movie.objects.annotate(
        num_booking=Count('booking')
    ).order_by('-num_booking')[:3]
    extra_context = extra_context or {}
    extra_context['total_revenue'] = total_revenue
    extra_context['popular_movies'] = popular_Movies
    extra_context['busiest_theaters'] = busiest_theaters
    return super().changelist_view(request, extra_context=extra_context)