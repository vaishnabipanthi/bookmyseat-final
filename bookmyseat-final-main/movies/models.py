from django.utils import timezone
import urllib.parse as urlparse
from django.db import models
from django.contrib.auth.models import User 


class Movie(models.Model):
    name= models.CharField(max_length=255)
    image= models.ImageField(upload_to="movies/")
    genre=models.CharField(max_length=100,default="Action")
    language=models.CharField(max_length=100,default="English")
    rating= models.DecimalField(max_digits=3,decimal_places=1)
    cast= models.TextField()
    description= models.TextField(blank=True,null=True) 
    trailer_address=models.URLField(max_length=200,blank=True,null=True,help_text="youtube link for the movies")
    @property
    def embed_url(self):
        if not self.trailer_address:
            return None
        url_data = urlparse.urlparse(self.trailer_address)
        query = urlparse.parse_qs(url_data.query)
        video_id = query.get("v")

        if video_id:
            return f"https://www.youtube.com/embed/{video_id[0]}"
        return None
    def __str__(self):
        return self.name
  

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='theaters')
    time= models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked=models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False) 
    reserved_at = models.DateTimeField(null=True, blank=True)
    reserved_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    seat=models.OneToOneField(Seat,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE)
    booked_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Booking by{self.user.username} for {self.seat.seat_number} at {self.theater.name}'