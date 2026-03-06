from django.urls import path
from django.contrib.auth import views as auth_views
from movies import views as movie_views
from . import views

class CustomLogoutView(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

urlpatterns = [
    path('',views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('logout/', CustomLogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('movies/',movie_views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/theaters/', movie_views.theater_list, name='theater_list'),
    path('theater/<int:theater_id>/seats/book/', movie_views.book_seats, name='book_seats'),
    path('payment/initiate/<str:amount>/<int:movie_id>/', movie_views.initiate_payment, name='initiate_payment'),
    path('payment-success/', movie_views.payment_success, name='payment_success'),
]
