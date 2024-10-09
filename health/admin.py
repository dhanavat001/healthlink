from django.contrib import admin
from .models import PatientProfile, DoctorProfile, HealthRecord, AIModel, Appointment, MedicalTest

admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(HealthRecord)
admin.site.register(AIModel)
admin.site.register(Appointment)
admin.site.register(MedicalTest)
