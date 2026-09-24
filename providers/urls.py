from django.urls import path
from . import views

app_name = 'providers'

urlpatterns = [
    path('', views.provider_list, name='provider_list'),
    path('<int:pk>/', views.provider_detail, name='provider_detail'),
    path('register/', views.register_provider, name='register_provider'),
    path('dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('edit/', views.edit_provider, name='edit_provider'),
]
