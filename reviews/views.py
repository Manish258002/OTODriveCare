from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from providers.models import Provider


@login_required
def add_review(request, provider_pk):
    provider = get_object_or_404(Provider, pk=provider_pk)
    existing = Review.objects.filter(user=request.user, provider=provider).first()
    if existing:
        messages.info(request, 'You have already reviewed this provider.')
        return redirect('providers:provider_detail', pk=provider_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.provider = provider
            review.save()
            messages.success(request, 'Review submitted!')
            return redirect('providers:provider_detail', pk=provider_pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form, 'provider': provider})


@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'reviews/my_reviews.html', {'reviews': reviews})
