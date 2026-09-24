from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('request/', views.request_help, name='request_help'),
    path('book/', views.book_service, name='book_service'),
    path('track/<int:pk>/', views.track_request, name='track_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('start/<int:pk>/', views.start_ride, name='start_ride'),
    path('complete/<int:pk>/', views.complete_request, name='complete_request'),
    path('update-location/<int:pk>/', views.update_rider_location, name='update_rider_location'),
    path('live-tracking/<int:pk>/', views.live_tracking, name='live_tracking'),
    path('payment/<int:pk>/', views.payment_page, name='payment_page'),
    path('confirm-payment/<int:pk>/', views.confirm_payment, name='confirm_payment'),
    path('online-paid/<int:pk>/', views.confirm_online_paid, name='confirm_online_paid'),
]
