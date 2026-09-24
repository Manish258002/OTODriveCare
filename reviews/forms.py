from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'class': 'form-control',
                                            'placeholder': 'Write your review...'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
