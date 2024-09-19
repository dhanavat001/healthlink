from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Appointment, AIModel, HealthRecord, PatientProfile, DoctorProfile, MedicalTest
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import HealthRecordForm, DoctorProfileForm, PatientProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages


@login_required
def add_doctor_profile(request):
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST)
        if form.is_valid():
            doctor_profile = form.save(commit=False)
            doctor_profile.user = request.user  # Link to the logged-in user
            doctor_profile.save()
            return redirect('doctor_dashboard')  # Redirect after saving
    else:
        form = DoctorProfileForm()
    
    return render(request, 'health/add_doctor.html', {'form': form})

@login_required
def add_patient_profile(request):
    if request.method == 'POST':
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            patient_profile = form.save(commit=False)
            patient_profile.user = request.user  # Link to the logged-in user
            patient_profile.save()
            return redirect('patient_dashboard')  # Redirect after saving
    else:
        form = PatientProfileForm()

    return render(request, 'health/add_patient.html', {'form': form})

@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)

    # Fetch doctor's appointments and patients
    appointments = Appointment.objects.filter(doctor=doctor)
    patients = PatientProfile.objects.filter(health_records__doctor=doctor).distinct()

    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.doctor = doctor  # Set current doctor
            health_record.save()
            return redirect('doctor_dashboard')
    else:
        form = HealthRecordForm()

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'patients': patients,
        'form': form
    }
    return render(request, 'health/doctordashboard.html', context)

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    health_records = HealthRecord.objects.filter(patient=patient)
    medical_tests = MedicalTest.objects.filter(health_record__patient=patient)

    context = {
        'patient': patient,
        'health_records': health_records,
        'medical_tests': medical_tests
    }
    return render(request, 'health/patient_detail.html', context)


@login_required
def upload_record(request):
    # Check if the logged-in user is a doctor
    if not hasattr(request.user, 'doctorprofile'):
        return HttpResponseForbidden("You are not authorized to upload health records.")
    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.doctor = request.user.doctorprofile  # Link the record to the logged-in doctor
            health_record.save()
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard after upload
    else:
        form = HealthRecordForm()

    return render(request, 'health/upload_record.html', {'form': form})


@login_required
def patient_dashboard(request):
    # Fetch data from models for the logged-in patient
    user = request.user
    medical_records = HealthRecord.objects.filter(patient=user)
    insights = AIModel.objects.filter(patient=user)
    appointments = Appointment.objects.filter(patient=user)
    # messages = Message.objects.filter(receiver=user)
    
    # Context to pass to template
    context = {
        'medical_records': medical_records,
        'insights': insights,
        'appointments': appointments,
        # 'messages': messages,
    }
    
    return render(request, 'health/patientdashboard.html', context)



@require_POST
def describe_problem(request):
    # Get the problem description from the form
    problem_description = request.POST.get('problem_description')

    if problem_description:
        # Create an instance of AIModel with the problem description
        ai_model = AIModel(problem_description=problem_description)
        ai_model.save()
        
        # Process the problem through the AI model to generate recommendations
        ai_model.process_problem()

        # Show success message to the user
        messages.success(request, 'Your problem has been submitted and processed by AI.')

        # Redirect to the dashboard or any other page
        return redirect('patient_dashboard')
    else:
        # Show error message if no description was provided
        messages.error(request, 'Please describe your problem.')
        return redirect('patient_dashboard')


@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Assign the current user as the patient
            appointment.save()
            return redirect('patient_dashboard')  # Redirect to the dashboard after scheduling
    else:
        form = AppointmentForm()
    
    return render(request, 'schedule_appointment.html', {'form': form})

def home(request):
    return render(request, 'health/home.html')