from django import forms
from datetime import time
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

class AMPMTimeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        hours = [(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)]
        minutes = [(str(i).zfill(2), str(i).zfill(2)) for i in range(60)]
        ampm = [('AM', 'AM'), ('PM', 'PM')]
        
        widgets = (
            forms.Select(attrs={'class': 'form-select'}, choices=hours),
            forms.Select(attrs={'class': 'form-select'}, choices=minutes),
            forms.Select(attrs={'class': 'form-select'}, choices=ampm),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, str):
                try:
                    h, m = value.split(':')[:2]
                    hour = int(h)
                    minute = int(m)
                except ValueError:
                    return [None, None, None]
            else:
                hour = value.hour
                minute = value.minute
            
            ampm = 'AM' if hour < 12 else 'PM'
            h = hour
            if hour == 0:
                h = 12
            elif hour > 12:
                h = hour - 12
            return [str(h).zfill(2), str(minute).zfill(2), ampm]
        return [None, None, None]

class AMPMTimeField(forms.MultiValueField):
    widget = AMPMTimeWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.ChoiceField(choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)]),
            forms.ChoiceField(choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(60)]),
            forms.ChoiceField(choices=[('AM', 'AM'), ('PM', 'PM')]),
        )
        super().__init__(fields, require_all_fields=True, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            h, m, ampm = data_list
            h = int(h)
            m = int(m)
            if ampm == 'PM' and h < 12:
                h += 12
            elif ampm == 'AM' and h == 12:
                h = 0
            return time(hour=h, minute=m)
        return None

class KundaliForm(forms.ModelForm):
    birth_time = AMPMTimeField(label="Time of Birth")

    class Meta:
        model = Kundali
        fields = ['name', 'dob', 'birth_time', 'birth_place', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State, Country'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (Optional)'}),
        }
