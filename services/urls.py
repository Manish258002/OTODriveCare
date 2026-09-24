from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('add/', views.add_service, name='add_service'),
    path('edit/<int:pk>/', views.edit_service, name='edit_service'),
    path('delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('nearby/', views.nearby_services, name='nearby_services'),
]
