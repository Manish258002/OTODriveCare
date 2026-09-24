from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Provider
from .forms import ProviderForm
from services.models import Service
from emergency.models import EmergencyRequest


def provider_list(request):
    providers = Provider.objects.filter(verified=True, is_available=True)
    return render(request, 'providers/provider_list.html', {'providers': providers})


def provider_detail(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    services = provider.service_set.all()
    reviews = provider.review_set.all()
    context = {'provider': provider, 'services': services, 'reviews': reviews}
    return render(request, 'providers/provider_detail.html', context)


@login_required
def register_provider(request):
    if hasattr(request.user, 'provider_profile'):
        return redirect('providers:provider_dashboard')
    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES)
        if form.is_valid():
            provider = form.save(commit=False)
            provider.owner = request.user
            provider.save()
            request.user.is_provider = True
            request.user.save()
            messages.success(request, 'Shop registered! Awaiting verification.')
            return redirect('providers:provider_dashboard')
    else:
        form = ProviderForm()
    return render(request, 'providers/register_provider.html', {'form': form})


@login_required
def provider_dashboard(request):
    if not request.user.is_provider:
        return redirect('accounts:register')
    provider = get_object_or_404(Provider, owner=request.user)
    requests = EmergencyRequest.objects.filter(provider=provider).order_by('-request_time')
    services = Service.objects.filter(provider=provider)
    context = {'provider': provider, 'requests': requests, 'services': services}
    return render(request, 'providers/provider_dashboard.html', context)


@login_required
def edit_provider(request):
    provider = get_object_or_404(Provider, owner=request.user)
    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES, instance=provider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop details updated!')
            return redirect('providers:provider_dashboard')
    else:
        form = ProviderForm(instance=provider)
    return render(request, 'providers/edit_provider.html', {'form': form})
