from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from emergency.models import EmergencyRequest
from reviews.models import Review


@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_panel:dashboard')
    if request.user.is_rider:
        return redirect('accounts:rider_dashboard')
    requests = EmergencyRequest.objects.filter(user=request.user).order_by('-request_time')[:8]
    reviews = Review.objects.filter(user=request.user).order_by('-date')[:5]
    context = {
        'requests': requests,
        'reviews': reviews,
        'total_requests': EmergencyRequest.objects.filter(user=request.user).count(),
    }
    return render(request, 'dashboard/user_dashboard.html', context)
