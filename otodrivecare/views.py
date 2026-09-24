from django.shortcuts import render, redirect
from django.contrib import messages
from providers.models import Provider
from reviews.models import Review
from services.models import SERVICE_CATALOG
from admin_panel.forms import AdminLoginForm
from otodrivecare.forms import ContactForm


def home(request):
    providers = Provider.objects.filter(verified=True)[:6]
    reviews = Review.objects.select_related('user', 'provider').order_by('-date')[:6]
    admin_form = AdminLoginForm(request)
    context = {
        'providers': providers,
        'reviews': reviews,
        'admin_form': admin_form,
        'catalog': SERVICE_CATALOG,
        'from_location': request.GET.get('from_location', ''),
        'to_location': request.GET.get('to_location', ''),
        'latitude': request.GET.get('latitude', ''),
        'longitude': request.GET.get('longitude', ''),
        'destination_latitude': request.GET.get('destination_latitude', ''),
        'destination_longitude': request.GET.get('destination_longitude', ''),
    }
    return render(request, 'public/home.html', context)


def services_page(request):
    return redirect('services:nearby_services')


def about(request):
    return render(request, 'public/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent to the admin team.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'public/contact.html', {'form': form})
