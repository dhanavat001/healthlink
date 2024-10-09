from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from AIModels.Django_Integration.disease_integration import predict_disease
from django.conf import settings
import os

# Patient Model
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()  # Required by default
    gender = models.CharField(max_length=10)  # Required by default
    address = models.TextField()
    medical_history = models.TextField()

    # Adding phone number with validation
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=False)  # Phone is required
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True) 

    def __str__(self):
        return self.user.username


# Doctor Model
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)
    
    # Adding phone number with validation
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=False)  # Phone is required
    
    age = models.IntegerField()  # Required field
    gender = models.CharField(max_length=10)  # Required field
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True) 

    def __str__(self):
        return self.user.username


# Health Record Model
class HealthRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='health_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    prescription = models.TextField()

    def __str__(self):
        return f'Record {self.id} for {self.patient.user.username}'


# AI Model
class AIModel(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    problem_description = models.TextField()
    recommended_doctor = models.CharField(max_length=100, blank=True, null=True)
    prognosis = models.CharField(max_length=100, blank=True, null=True)
    ai_insights = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'AIModel for Problem: {self.problem_description[:30]}'

# Appointment Model
class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE) 
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Appointment with {self.doctor} on {self.date} at {self.time}'

# Medical Test Model
class MedicalTest(models.Model):
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    test_result = models.TextField()
    test_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Test {self.test_name} for Record {self.health_record.id}'
