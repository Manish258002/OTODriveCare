from django import forms
from .models import Provider


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = [
            'shop_name', 'phone', 'email', 'address',
            'latitude', 'longitude', 'opening_time',
            'closing_time', 'shop_image', 'is_available'
        ]
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
