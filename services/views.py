from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service, SERVICE_CATALOG
from .forms import ServiceForm
from providers.models import Provider


@login_required
def add_service(request):
    provider = get_object_or_404(Provider, owner=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = provider
            service.save()
            messages.success(request, 'Service added successfully!')
            return redirect('providers:provider_dashboard')
    else:
        form = ServiceForm()
    return render(request, 'services/add_service.html', {'form': form})


@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk, provider__owner=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated!')
            return redirect('providers:provider_dashboard')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/edit_service.html', {'form': form, 'service': service})


@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk, provider__owner=request.user)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted.')
        return redirect('providers:provider_dashboard')
    return render(request, 'services/confirm_delete.html', {'service': service})


def nearby_services(request):
    from_location = request.GET.get('from_location', '')
    to_location = request.GET.get('to_location', '')
    return render(request, 'services/nearby_services.html', {
        'catalog': SERVICE_CATALOG,
        'from_location': from_location,
        'to_location': to_location,
        'latitude': request.GET.get('latitude', ''),
        'longitude': request.GET.get('longitude', ''),
        'destination_latitude': request.GET.get('destination_latitude', ''),
        'destination_longitude': request.GET.get('destination_longitude', ''),
    })
