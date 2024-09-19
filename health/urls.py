from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('upload_record/', views.upload_record, name='upload_record'),
    path('schedule_appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('describe_problem/', views.describe_problem, name='describe_problem'),
    path('add-doctor-profile/', views.add_doctor_profile, name='add_doctor_profile'),
    path('add-patient-profile/', views.add_patient_profile, name='add_patient_profile'),
]
