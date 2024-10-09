from django import forms
from .models import Appointment, DoctorProfile, PatientProfile, HealthRecord, MedicalTest
from django import forms


class MedicalTestForm(forms.ModelForm):
    class Meta:
        model = MedicalTest
        fields = ['health_record', 'test_name', 'test_result']  # Include health_record in fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['health_record'] = forms.ModelChoiceField(
            queryset=HealthRecord.objects.all(), 
            empty_label="Select Health Record",  
            widget=forms.Select(attrs={'class': 'form-control'})  
        )
        self.fields['test_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['test_result'].widget.attrs.update({'class': 'form-control', 'rows': 3})


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['patient', 'symptoms', 'diagnosis', 'prescription']
        
        # Adding widgets to each field for proper Bootstrap styling
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Select a patient'}),
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter symptoms here'}),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter diagnosis here'}),
            'prescription': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter prescription here'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'notes']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a patient'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

# Form for DoctorProfile
class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'license_number', 'phone_number', 'age', 'gender', 'profile_image']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')], attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Form for PatientProfile
class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['age', 'gender', 'address', 'medical_history', 'phone_number', 'profile_image']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')], attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

