from django.db import models
from accounts.models import User
from providers.models import Provider

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'provider']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} → {self.provider.shop_name} ({self.rating}★)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update provider's average rating
        provider = self.provider
        reviews = Review.objects.filter(provider=provider)
        provider.rating = sum(r.rating for r in reviews) / reviews.count()
        provider.save()
