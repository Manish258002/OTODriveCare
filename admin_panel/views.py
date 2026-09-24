from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import User
from providers.models import Provider
from emergency.models import EmergencyRequest
from reviews.models import Review
from dashboard.models import ContactMessage, Complaint
from .decorators import admin_required
from .forms import AdminLoginForm


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:dashboard')
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_staff:
                messages.error(request, 'Access denied. Admin credentials only.')
            else:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('admin_panel:dashboard')
        else:
            messages.error(request, 'Invalid admin username or password.')
    else:
        form = AdminLoginForm()
    return render(request, 'admin_panel/login.html', {'form': form})


def admin_logout(request):
    logout(request)
    messages.info(request, 'Admin logged out successfully.')
    return redirect('landing')


@admin_required
def dashboard(request):
    context = {
        'total_users': User.objects.filter(is_staff=False, is_provider=False).count(),
        'total_providers': Provider.objects.count(),
        'total_requests': EmergencyRequest.objects.count(),
        'pending_requests': EmergencyRequest.objects.filter(status='Pending').count(),
        'total_reviews': Review.objects.count(),
        'unread_contacts': ContactMessage.objects.filter(is_read=False).count(),
        'open_complaints': Complaint.objects.filter(admin_reply='').count(),
        'recent_requests': EmergencyRequest.objects.select_related('user', 'provider').order_by('-request_time')[:8],
        'recent_contacts': ContactMessage.objects.order_by('-created_at')[:5],
        'recent_users': User.objects.filter(is_staff=False).order_by('-created_at')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def users_list(request):
    q = request.GET.get('q', '')
    users = User.objects.filter(is_staff=False, is_rider=False).order_by('-created_at')
    if q:
        users = users.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))
    return render(request, 'admin_panel/users.html', {'users': users, 'q': q})


@admin_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk, is_staff=False)
    requests = EmergencyRequest.objects.filter(user=user).order_by('-request_time')
    reviews = Review.objects.filter(user=user).select_related('provider')
    return render(request, 'admin_panel/user_detail.html', {
        'profile_user': user,
        'requests': requests,
        'reviews': reviews,
    })


@admin_required
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk, is_staff=False)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {user.username} {status}.')
    return redirect('admin_panel:users')


@admin_required
def reviews_list(request):
    reviews = Review.objects.select_related('user', 'provider').order_by('-date')
    return render(request, 'admin_panel/reviews.html', {'reviews': reviews})


@admin_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('admin_panel:reviews')


@admin_required
def emergency_list(request):
    status = request.GET.get('status', '')
    requests_qs = EmergencyRequest.objects.select_related('user', 'provider').order_by('-request_time')
    if status:
        requests_qs = requests_qs.filter(status=status)
    return render(request, 'admin_panel/emergency_requests.html', {
        'requests': requests_qs,
        'status': status,
        'status_choices': EmergencyRequest._meta.get_field('status').choices,
    })


@admin_required
def emergency_detail(request, pk):
    req = get_object_or_404(EmergencyRequest, pk=pk)
    return render(request, 'admin_panel/emergency_detail.html', {'req': req})


@admin_required
def history(request):
    requests_qs = EmergencyRequest.objects.select_related('user', 'provider').order_by('-request_time')
    return render(request, 'admin_panel/history.html', {'requests': requests_qs})


@admin_required
def complaints_list(request):
    complaints = Complaint.objects.select_related('user').order_by('-created_at')
    return render(request, 'admin_panel/complaints.html', {'complaints': complaints})


@admin_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        reply = request.POST.get('admin_reply', '').strip()
        if reply:
            complaint.admin_reply = reply
            complaint.replied_at = timezone.now()
            complaint.save()
            messages.success(request, 'Reply saved.')
        else:
            messages.error(request, 'Reply cannot be empty.')
        return redirect('admin_panel:complaint_detail', pk=pk)
    return render(request, 'admin_panel/complaint_detail.html', {'complaint': complaint})


@admin_required
def contacts_list(request):
    contacts = ContactMessage.objects.order_by('-created_at')
    return render(request, 'admin_panel/contacts.html', {'contacts': contacts})


@admin_required
def contact_detail(request, pk):
    contact = get_object_or_404(ContactMessage, pk=pk)
    if not contact.is_read:
        contact.is_read = True
        contact.save()

    if request.method == 'POST':
        reply = request.POST.get('reply_message', '').strip()
        if reply:
            contact.reply_message = reply
            contact.replied_at = timezone.now()
            contact.save()
            send_mail(
                subject='Reply from OTO Drive Care',
                message=reply,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact.email],
                fail_silently=False,
            )
            messages.success(request, 'Reply sent to customer.')
        else:
            messages.error(request, 'Reply cannot be empty.')
        return redirect('admin_panel:contact_detail', pk=pk)

    return render(request, 'admin_panel/contact_detail.html', {'contact': contact})


@admin_required
def contact_delete(request, pk):
    contact = get_object_or_404(ContactMessage, pk=pk)
    contact.delete()
    messages.success(request, 'Contact message deleted.')
    return redirect('admin_panel:contacts')


@admin_required
def providers_list(request):
    providers = Provider.objects.select_related('owner').order_by('-created_at')
    return render(request, 'admin_panel/providers.html', {'providers': providers})


@admin_required
def provider_toggle_verified(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    provider.verified = not provider.verified
    provider.save()
    messages.success(request, f'{provider.shop_name} verification updated.')
    return redirect('admin_panel:providers')
