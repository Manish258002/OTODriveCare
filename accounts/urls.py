from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('rider-register/', views.rider_register, name='rider_register'),
    path('login/', views.user_login, name='login'),
    path('rider-login/', views.rider_login, name='rider_login'),
    path('rider-dashboard/', views.rider_dashboard, name='rider_dashboard'),
    path('rider-duty/', views.rider_toggle_duty, name='rider_toggle_duty'),
    path('rider-history/', views.rider_history, name='rider_history'),
    path('rider-alerts/', views.rider_alerts_api, name='rider_alerts'),
    path('rider-request/accept/<int:pk>/', views.rider_accept_request, name='rider_accept_request'),
    path('rider-request/decline/<int:pk>/', views.rider_decline_request, name='rider_decline_request'),
    path('rider-request/verify/<int:pk>/', views.rider_verify_code, name='rider_verify_code'),
    path('complaint/', views.complaint, name='complaint'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.change_password, name='settings'),
    path('change-password/', views.change_password, name='change_password'),
    path('wallet/', views.wallet, name='wallet'),
]
