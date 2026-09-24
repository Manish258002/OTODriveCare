from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/', include('admin_panel.urls')),
    path('', views.home, name='home'),
    path('login/', RedirectView.as_view(pattern_name='accounts:login', permanent=False)),
    path('landing/', views.home, name='landing'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('service/', views.services_page, name='service'),
    path('accounts/', include('accounts.urls')),
    path('providers/', include('providers.urls')),
    path('services/', include('services.urls')),
    path('breakdown/', include('breakdown.urls')),
    path('emergency/', include('emergency.urls')),
    path('reviews/', include('reviews.urls')),
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
