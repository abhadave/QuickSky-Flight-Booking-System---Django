from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('book/<int:id>/', views.book_flight, name='book_flight'),
    path('booking_list/',views.booking_list,name='booking_list'),
    path('confirm/<int:id>/', views.confirm_booking, name='confirm_booking'),
    path('cancel/<int:id>/', views.cancel_booking, name='cancel_booking'),
    path('history', views.booking_history, name='booking_history'),
    path('about_us', views.about_us, name='about_us'),
    path('update/<int:pk>/', views.update, name='update'),
    path("payment/<int:id>/", views.payment_view, name="payment"),
   



]


