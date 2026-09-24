from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
import math

from .models import EmergencyRequest
from .forms import EmergencyRequestForm
from services.models import SERVICE_CATALOG, catalog_price


def generate_confirmation_code():
    import secrets
    return ''.join(secrets.choice('0123456789') for _ in range(4))


def calculate_distance_km(lat1, lon1, lat2, lon2):
    if not lat1 or not lon1 or not lat2 or not lon2:
        return 1.0
    delta_lat = abs(lat2 - lat1) * 111
    delta_lon = abs(lon2 - lon1) * 111
    return round(max(math.hypot(delta_lat, delta_lon), 1.0), 2)


@login_required
def request_help(request):
    initial_data = {
        'service_type': request.GET.get('service_type', 'tire'),
        'from_location': request.GET.get('from_location', ''),
        'to_location': request.GET.get('to_location', ''),
    }

    if request.method == 'POST':
        form = EmergencyRequestForm(request.POST, request.FILES)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.user = request.user
            emergency.provider = None
            emergency.status = 'Pending'
            lat = form.cleaned_data['latitude'] or 0.0
            lon = form.cleaned_data['longitude'] or 0.0
            dest_lat = form.cleaned_data.get('destination_latitude') or lat
            dest_lon = form.cleaned_data.get('destination_longitude') or lon
            service_type = form.cleaned_data['service_type']
            distance_km = calculate_distance_km(lat, lon, dest_lat, dest_lon)
            emergency.total_fare = round(float(catalog_price(service_type)) + (distance_km * 8), 2)
            emergency.save()
            messages.success(request, 'Finding a nearby technician. Please wait for a rider to accept.')
            return redirect('emergency:track_request', pk=emergency.pk)
    else:
        form = EmergencyRequestForm(initial=initial_data)
    return render(request, 'emergency/request_help.html', {
        'form': form,
        'catalog': SERVICE_CATALOG,
    })


@login_required
def book_service(request):
    if request.method != 'POST':
        return redirect('services:nearby_services')

    service_type = request.POST.get('service_type', 'tire')
    from_location = request.POST.get('from_location', '')
    to_location = request.POST.get('to_location', '')
    try:
        latitude = float(request.POST.get('latitude') or 0)
        longitude = float(request.POST.get('longitude') or 0)
        dest_lat = float(request.POST.get('destination_latitude') or 0)
        dest_lon = float(request.POST.get('destination_longitude') or 0)
    except (TypeError, ValueError):
        latitude = longitude = dest_lat = dest_lon = 0
    if not from_location.strip() or not to_location.strip() or not all(-90 <= value <= 90 for value in (latitude, dest_lat)) or not all(-180 <= value <= 180 for value in (longitude, dest_lon)) or (latitude == 0 and longitude == 0):
        messages.error(request, 'Select pickup and drop locations on the map before booking.')
        return redirect('services:nearby_services')
    vehicle_type = request.POST.get('vehicle_type', 'car')
    description = request.POST.get('description') or f'{service_type.replace("_", " ").title()} service requested'

    distance_km = calculate_distance_km(latitude, longitude, dest_lat, dest_lon)
    fare = round(float(catalog_price(service_type)) + (distance_km * 8), 2)

    emergency = EmergencyRequest.objects.create(
        user=request.user,
        service_type=service_type,
        from_location=from_location,
        to_location=to_location,
        vehicle_type=vehicle_type,
        description=description,
        latitude=latitude,
        longitude=longitude,
        destination_latitude=dest_lat,
        destination_longitude=dest_lon,
        total_fare=fare,
        status='Pending',
    )
    messages.success(request, 'Searching for an on-duty rider...')
    return redirect('emergency:track_request', pk=emergency.pk)


@login_required
def track_request(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk)
    provider_owner = req.provider.owner if req.provider else None
    if request.user != req.user and request.user != provider_owner and not request.user.is_staff:
        return redirect('home')
    return render(request, 'emergency/track_request.html', {'req': req})


@login_required
def my_requests(request):
    if request.user.is_rider:
        return redirect('accounts:rider_history')
    reqs = EmergencyRequest.objects.filter(user=request.user)
    return render(request, 'emergency/my_requests.html', {'requests': reqs})


@login_required
def start_ride(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk, provider__owner=request.user)
    if not req.code_verified:
        messages.error(request, 'Verify the confirmation code before starting the ride.')
        return redirect('accounts:rider_dashboard')
    req.status = 'On the way'
    req.save(update_fields=['status'])
    messages.success(request, 'Ride started.')
    return redirect('emergency:track_request', pk=req.pk)


@login_required
def complete_request(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk, provider__owner=request.user)
    req.status = 'Completed'
    req.completed_time = timezone.now()
    req.save(update_fields=['status', 'completed_time'])
    messages.success(request, 'Ride finished. Choose a payment method.')
    return redirect('emergency:payment_page', pk=req.pk)


@login_required
def update_rider_location(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk)
    provider_owner = req.provider.owner if req.provider else None
    if request.user != provider_owner:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        if lat and lon:
            try:
                req.rider_latitude = float(lat)
                req.rider_longitude = float(lon)
            except ValueError:
                return JsonResponse({'error': 'Invalid location'}, status=400)
            req.save(update_fields=['rider_latitude', 'rider_longitude'])
            return JsonResponse({'status': 'ok', 'latitude': req.rider_latitude, 'longitude': req.rider_longitude})
        return JsonResponse({'error': 'Missing location'}, status=400)

    return JsonResponse({
        'status': req.status,
        'latitude': req.rider_latitude,
        'longitude': req.rider_longitude,
    })


@login_required
def live_tracking(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk)
    provider_owner = req.provider.owner if req.provider else None
    if request.user != req.user and request.user != provider_owner and not request.user.is_staff:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    return JsonResponse({
        'status': req.status,
        'customer_latitude': req.latitude,
        'customer_longitude': req.longitude,
        'rider_latitude': req.rider_latitude,
        'rider_longitude': req.rider_longitude,
        'confirmation_code': req.confirmation_code,
        'code_verified': req.code_verified,
        'provider_name': req.provider.shop_name if req.provider else '',
        'payment_method': req.payment_method,
        'payment_completed': req.payment_completed,
    })


@login_required
def payment_page(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk)
    provider_owner = req.provider.owner if req.provider else None
    if request.user != req.user and request.user != provider_owner and not request.user.is_staff:
        return redirect('home')
    show_qr = request.GET.get('method') == 'online' or req.payment_method == 'Online'
    return render(request, 'emergency/payment.html', {'req': req, 'show_qr': show_qr})


def _after_payment_home(user):
    if user.is_rider:
        return redirect('accounts:rider_dashboard')
    if user.is_staff:
        return redirect('admin_panel:dashboard')
    return redirect('home')


@login_required
def confirm_payment(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk)
    provider_owner = req.provider.owner if req.provider else None
    if request.user != req.user and request.user != provider_owner and not request.user.is_staff:
        return redirect('home')

    method = request.POST.get('payment_method', 'Cash')
    req.payment_method = method
    req.status = 'Completed'
    if not req.completed_time:
        req.completed_time = timezone.now()

    if method == 'Online':
        req.payment_completed = False
        req.save()
        messages.info(request, 'Scan the QR code to pay online.')
        from django.urls import reverse
        return redirect(reverse('emergency:payment_page', args=[pk]) + '?method=online')

    req.payment_completed = True
    req.save()
    messages.success(request, 'Cash payment selected. Ride closed.')
    return _after_payment_home(request.user)


@login_required
@require_POST
def confirm_online_paid(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk)
    provider_owner = req.provider.owner if req.provider else None
    if request.user != provider_owner and not request.user.is_staff:
        return redirect('home')
    req.payment_method = 'Online'
    req.payment_completed = True
    req.status = 'Completed'
    if not req.completed_time:
        req.completed_time = timezone.now()
    req.save()
    messages.success(request, 'Online payment completed. Ride closed.')
    return _after_payment_home(request.user)
