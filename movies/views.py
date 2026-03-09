import razorpay
from django.utils import timezone  
from datetime import timedelta 
from django.conf import settings
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import send_mail

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

def movie_list(request):
    movies = Movie.objects.all()     
    genre_query = request.GET.get('genre')
    language_query = request.GET.get('language')
    if genre_query and genre_query!="":
        movies = movies.filter(genre__iexact=genre_query)
    if language_query and language_query!="":
        movies = movies.filter(language__iexact=language_query)
    print("GET (movies page):", request.GET)
    print("Movies after filter:", movies.count())  
    return render(request, 'movies/movie_list.html', {'movies': movies})

def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})
  

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html',{'movie':movie,'theaters':theaters})

def initiate_payment(request,amount,movie_id):
    #client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    #data = {
     #   "amount": int(amount) * 100,
      #  "currency": "INR",
       # "receipt": f"receipt_{movie_id}",
        #"payment_capture": 1
    #}
    #razorpay_order = client.order.create(data=data)
    context = {
        "order_id": "dummy_order_id",
        "amount": amount,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "movie_id": movie_id ,
    }
    return render(request, 'movies/payment.html', context)


@login_required(login_url='/login/')
def book_seats(request,theater_id):
    theater=get_object_or_404(Theater,id=theater_id)
    expired_time = timezone.now() - timedelta(minutes=5)
    Seat.objects.filter(
        theater=theater,
        is_reserved=True,
        reserved_at__lt=expired_time,
        is_booked=False
     ).update(is_reserved=False, reserved_by=None, reserved_at=None)
    
    seats=Seat.objects.filter(theater=theater)
    if request.method=='POST':
        selected_seats= request.POST.getlist('seats')

        if not selected_seats:
            return render(request,"movies/seat_selection.html",{'theater':theater,"seats":seats,'error':"No seat selected"})
        for seat_id in selected_seats:
            seat=get_object_or_404(Seat,id=seat_id,theater=theater)
            if seat.is_booked or (seat.is_reserved and seat.reserved_by != request.user):
                return render(request,"movies/seat_selection.html",{'theater':theater,"seats":seats,'error':f"Seat {seat.seat_number} is already booked"})
            seat.is_reserved = True
            seat.reserved_by = request.user
            seat.reserved_at = timezone.now()
            seat.save()

            request.session['selected_seats'] = selected_seats
            request.session['current_theater_id'] = theater_id
            total_amount = len(selected_seats) * 200
            return redirect('initiate_payment', amount=total_amount, movie_id=theater.movie.id)
    return render(request,"movies/seat_selection.html",{'theater':theater,"seats":seats})

def payment_success(request):
    selected_seats = request.session.get('selected_seats')
    theater_id = request.session.get('current_theater_id')
    
    if not selected_seats or not theater_id:
        return redirect('home')
    theater = get_object_or_404(Theater, id=theater_id)
    movie_obj = theater.movie
    booked_seats_number = []
    
    for seat_id in selected_seats:
        seat = get_object_or_404(Seat, id=seat_id, theater=theater)
        Booking.objects.get_or_create(
            user=request.user,
                seat=seat,
                movie=movie_obj,
                theater=theater
            )
        seat.is_booked = True
        seat.is_reserved = False
        seat.reserved_by = None
        seat.reserved_at = None
        seat.save()
        booked_seats_number.append(seat.seat_number)

    subject = 'Booking Confirmation'
    seat_str = ', '.join(booked_seats_number)
    message = (
      f"Hi {request.user.username},\n\n"
      f"Your booking for {movie_obj.name} at {theater.name} is successful.\n"
      f"Theater: {theater.name}\n"
      f"seats: {seat_str}\n\n"
      "Enjoy your movie!"
    )

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [request.user.email])
    except Exception as e:
        print(f"Mail sending failed: {e}")
    
    if 'selected_seats' in request.session:
     del request.session['selected_seats']
    if 'current_theater_id' in request.session:
     del request.session['current_theater_id']
    return render(request, 'movies/payment_success.html', {'theater': theater, 'booked_seats': booked_seats_number})  