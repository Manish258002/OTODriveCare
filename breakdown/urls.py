from django.urls import path
from . import views

app_name = 'breakdown'

urlpatterns = [
    path('', views.breakdown_redirect, name='breakdown'),
]
