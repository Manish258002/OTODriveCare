from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users_list, name='users'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/toggle/', views.user_toggle_active, name='user_toggle'),
    path('reviews/', views.reviews_list, name='reviews'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('emergency/', views.emergency_list, name='emergency'),
    path('emergency/<int:pk>/', views.emergency_detail, name='emergency_detail'),
    path('history/', views.history, name='history'),
    path('complaints/', views.complaints_list, name='complaints'),
    path('complaints/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('contacts/', views.contacts_list, name='contacts'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('providers/', views.providers_list, name='providers'),
    path('providers/<int:pk>/verify/', views.provider_toggle_verified, name='provider_verify'),
]
