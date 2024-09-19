from django import forms
from .models import Appointment, DoctorProfile, PatientProfile, HealthRecord

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['patient', 'symptoms', 'diagnosis', 'prescription']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'license_number']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['age', 'gender', 'address', 'medical_history']
