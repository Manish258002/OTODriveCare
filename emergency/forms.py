from django import forms
from .models import EmergencyRequest


class EmergencyRequestForm(forms.ModelForm):
    class Meta:
        model = EmergencyRequest
        fields = [
            'service_type', 'from_location', 'to_location', 'vehicle_type',
            'description', 'latitude', 'longitude', 'destination_latitude',
            'destination_longitude', 'photo'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control',
                                                  'placeholder': 'Describe your problem...'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'destination_latitude': forms.HiddenInput(),
            'destination_longitude': forms.HiddenInput(),
            'from_location': forms.TextInput(attrs={'placeholder': 'From location'}),
            'to_location': forms.TextInput(attrs={'placeholder': 'To location'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].widget.attrs['class'] = 'form-select'
        self.fields['vehicle_type'].widget.attrs['class'] = 'form-select'
        self.fields['from_location'].widget.attrs['class'] = 'form-control'
        self.fields['to_location'].widget.attrs['class'] = 'form-control'
        for name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
