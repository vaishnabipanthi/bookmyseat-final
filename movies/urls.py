from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('theaters/<int:movie_id>/', views.theater_list, name='theater_list'),
    path('theater/<int:theater_id>/seats/book', views.book_seats, name='book_seats'),
    
]
