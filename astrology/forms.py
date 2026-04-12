from django import forms
from .models import PalmReading, Kundali

class PalmReadingForm(forms.ModelForm):
    class Meta:
        model = PalmReading
        fields = ['image', 'name', 'address', 'phone']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'id': 'palm-image-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Full Address', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }
        labels = {
            'image': 'Upload Right Hand Image'
        }

class KundaliForm(forms.ModelForm):
    class Meta:
        model = Kundali
        fields = ['name', 'dob', 'birth_time', 'birth_place', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'birth_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State, Country'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (Optional)'}),
        }
