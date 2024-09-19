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


# AI Model
class AIModel(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    problem_description = models.TextField()
    recommended_doctor = models.CharField(max_length=100, blank=True, null=True)
    ai_insights = models.TextField(blank=True, null=True)

    def process_problem(self):
        # Logic to simulate AI recommendations
        if "cardio" in self.problem_description.lower():
            self.recommended_doctor = "Dr. John, Cardiologist"
        elif "diabetes" in self.problem_description.lower():
            self.recommended_doctor = "Dr. Smith, Endocrinologist"
        else:
            self.recommended_doctor = "General Physician"
        
        # Generate some AI insights based on problem description
        self.ai_insights = "AI suggests further tests based on the input."
        self.save()

    def __str__(self):
        return f'AIModel for Problem: {self.problem_description[:30]}'


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
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.CharField(max_length=100)
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
