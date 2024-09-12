from django.db import models
from django.contrib.auth.models import User

# Patient Model
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    medical_history = models.TextField()

    def __str__(self):
        return self.user.username

# Doctor Model
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=100)

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

# AI Model - For Predictive Analytics
class AIModel(models.Model):
    model_name = models.CharField(max_length=100)
    version = models.CharField(max_length=10)
    description = models.TextField()
    date_trained = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.model_name} (v{self.version})'

# Model Prediction - AI Model Results
class ModelPrediction(models.Model):
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE)
    prediction_result = models.TextField()
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Prediction {self.id} by {self.ai_model.model_name}'

# Appointment Model
class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed')])

    def __str__(self):
        return f'Appointment {self.id} on {self.appointment_date}'

# Medical Test Model
class MedicalTest(models.Model):
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    test_result = models.TextField()
    test_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Test {self.test_name} for Record {self.health_record.id}'
