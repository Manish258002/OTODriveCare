from emergency.models import EmergencyRequest


def rider_alerts(request):
    pending = 0
    active = None
    if getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'is_rider', False):
        pending = EmergencyRequest.objects.filter(status='Pending').count()
        active = EmergencyRequest.objects.filter(
            provider__owner=request.user,
            status__in=['Accepted', 'On the way'],
        ).first()
    return {
        'pending_ride_count': pending,
        'active_ride': active,
    }
