from datetime import time
import random
import string
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from dashboard.forms import ComplaintForm
from dashboard.models import Complaint
from emergency.models import EmergencyRequest
from providers.models import Provider
from .models import Wallet, WalletTransaction

from .forms import (
    CustomPasswordChangeForm,
    RiderRegisterForm,
    UserLoginForm,
    UserProfileForm,
    UserRegisterForm,
)


def make_code():
    return ''.join(random.choices(string.digits, k=4))


def ensure_rider_provider(user):
    provider = Provider.objects.filter(owner=user).first()
    if provider is None:
        provider = Provider.objects.create(
            owner=user,
            shop_name=f'{user.username} Technician',
            phone=user.phone or '0000000000',
            email=user.email or '',
            address=user.location or 'On-road automobile technician',
            opening_time=time(9, 0),
            closing_time=time(21, 0),
            verified=True,
            is_available=user.on_duty,
        )
    return provider


def register(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_panel:dashboard')
        if request.user.is_rider:
            return redirect('accounts:rider_dashboard')
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_panel:dashboard')
        if request.user.is_rider:
            return redirect('accounts:rider_dashboard')
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                messages.error(request, 'Please use Admin Login from the navbar.')
                return redirect('accounts:login')
            if user.is_rider:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('accounts:rider_dashboard')
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def rider_register(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_panel:dashboard')
        if request.user.is_rider:
            return redirect('accounts:rider_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = RiderRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Rider account created successfully!')
            return redirect('accounts:rider_dashboard')
    else:
        form = RiderRegisterForm()
    return render(request, 'accounts/rider_register.html', {'form': form})


def rider_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_panel:dashboard')
        if request.user.is_rider:
            return redirect('accounts:rider_dashboard')
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_rider:
                messages.error(request, 'Access denied. Rider credentials only.')
                return redirect('accounts:rider_login')
            login(request, user)
            messages.success(request, f'Welcome rider, {user.username}!')
            return redirect('accounts:rider_dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/rider_login.html', {'form': form})


@login_required
def rider_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_panel:dashboard')
    if not request.user.is_rider:
        return redirect('accounts:login')

    provider = ensure_rider_provider(request.user)
    pending = EmergencyRequest.objects.filter(status='Pending').order_by('-request_time')
    my_active = EmergencyRequest.objects.filter(
        provider=provider,
        status__in=['Accepted', 'On the way'],
    ).order_by('-request_time')
    history = EmergencyRequest.objects.filter(provider=provider).exclude(
        status__in=['Pending', 'Accepted', 'On the way']
    )[:8]
    return render(request, 'accounts/rider_dashboard.html', {
        'requests': pending,
        'active_rides': my_active,
        'history': history,
        'provider': provider,
    })


@login_required
def wallet(request):
    item, _ = Wallet.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
        except (InvalidOperation, TypeError):
            amount = Decimal('0')
        action = request.POST.get('action')
        if amount <= 0:
            messages.error(request, 'Enter a valid amount.')
        elif action == WalletTransaction.ADD:
            item.balance += amount
            item.save(update_fields=['balance', 'updated_at'])
            WalletTransaction.objects.create(wallet=item, transaction_type=action, amount=amount)
            messages.success(request, 'Money added to your wallet.')
        elif action == WalletTransaction.WITHDRAW and item.balance >= amount:
            item.balance -= amount
            item.save(update_fields=['balance', 'updated_at'])
            WalletTransaction.objects.create(wallet=item, transaction_type=action, amount=amount)
            messages.success(request, 'Withdrawal recorded.')
        else:
            messages.error(request, 'Insufficient wallet balance.')
        return redirect('accounts:wallet')
    return render(request, 'accounts/wallet.html', {
        'wallet': item,
        'transactions': item.transactions.all()[:10],
    })


@login_required
@require_POST
def rider_toggle_duty(request):
    if not request.user.is_rider:
        return redirect('accounts:login')
    provider = ensure_rider_provider(request.user)
    request.user.on_duty = not request.user.on_duty
    request.user.save(update_fields=['on_duty'])
    provider.is_available = request.user.on_duty
    provider.save(update_fields=['is_available'])
    if request.user.on_duty:
        messages.success(request, 'You are On Duty. Allow location so nearby jobs can reach you.')
    else:
        messages.info(request, 'You are Off Duty. New job notifications are paused.')
    return redirect('accounts:rider_dashboard')


@login_required
def rider_accept_request(request, pk):
    if not request.user.is_rider:
        return redirect('accounts:login')
    if not request.user.on_duty:
        messages.error(request, 'Turn On Duty before accepting a ride.')
        return redirect('accounts:rider_dashboard')

    req = get_object_or_404(EmergencyRequest, pk=pk, status='Pending')
    rider_provider = ensure_rider_provider(request.user)
    req.provider = rider_provider
    req.status = 'Accepted'
    req.accepted_time = timezone.now()
    if not req.confirmation_code:
        req.confirmation_code = make_code()
    req.save()
    messages.success(request, 'Ride accepted. Ask the customer for the confirmation code.')
    return redirect('accounts:rider_dashboard')


@login_required
def rider_decline_request(request, pk):
    if not request.user.is_rider:
        return redirect('accounts:login')
    req = get_object_or_404(EmergencyRequest, pk=pk, status='Pending')
    req.status = 'Cancelled'
    req.save(update_fields=['status'])
    messages.info(request, 'Ride request declined.')
    return redirect('accounts:rider_dashboard')


@login_required
@require_POST
def rider_verify_code(request, pk):
    if not request.user.is_rider:
        return redirect('accounts:login')
    req = get_object_or_404(EmergencyRequest, pk=pk, provider__owner=request.user)
    code = (request.POST.get('confirmation_code') or '').strip().upper()
    if code and code == (req.confirmation_code or '').upper():
        req.code_verified = True
        req.status = 'On the way'
        req.save(update_fields=['code_verified', 'status'])
        messages.success(request, 'Code verified. Map opened to the pickup location. Start the ride.')
        return redirect('emergency:track_request', pk=req.pk)
    messages.error(request, 'Invalid confirmation code.')
    return redirect('accounts:rider_dashboard')


@login_required
def rider_history(request):
    if not request.user.is_rider:
        return redirect('accounts:login')
    provider = ensure_rider_provider(request.user)
    history = EmergencyRequest.objects.filter(provider=provider)
    return render(request, 'accounts/rider_history.html', {'requests': history})


@login_required
def rider_alerts_api(request):
    if not request.user.is_rider:
        return JsonResponse({'count': 0, 'requests': []})
    pending_qs = EmergencyRequest.objects.filter(status='Pending').order_by('-request_time')
    pending = list(pending_qs[:8])
    return JsonResponse({
        'count': pending_qs.count(),
        'on_duty': request.user.on_duty,
        'requests': [
            {
                'id': item.pk,
                'service': item.get_service_type_display(),
                'from': item.from_location,
                'to': item.to_location,
                'fare': str(item.total_fare),
            }
            for item in pending
        ],
    })


@login_required
def complaint(request):
    role = 'rider' if request.user.is_rider else 'user'
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.role = role
            item.save()
            messages.success(request, 'Complaint submitted to admin.')
            return redirect('accounts:complaint')
    else:
        form = ComplaintForm()
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'accounts/complaint.html', {'form': form, 'complaints': complaints})


@login_required
def profile(request):
    if request.user.is_staff:
        return redirect('admin_panel:dashboard')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password(request):
    if request.user.is_staff:
        return redirect('admin_panel:dashboard')
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
