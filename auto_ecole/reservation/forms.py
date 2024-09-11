from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['nom', 'email', 'date_reservation', 'heure_reservation', 'type_vehicule']
        widgets = {
            'date_reservation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_reservation': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
