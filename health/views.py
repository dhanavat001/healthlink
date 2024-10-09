from django.shortcuts import render, redirect
from .forms import AppointmentForm, MedicalTestForm
from .models import Appointment, AIModel, HealthRecord, PatientProfile, DoctorProfile, MedicalTest
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from .forms import HealthRecordForm, DoctorProfileForm, PatientProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from AIModels.Django_Integration.disease_integration import predict_disease, predict_doctor
from AIModels.Gemini.insights import generate_insights


def check_user_profile(request):
    user = request.user

    # Check if the user is authenticated
    if not user.is_authenticated:
        return HttpResponse("<p>Please login to access this feature.</p>")

    # Check if user has a PatientProfile or DoctorProfile
    has_patient_profile = PatientProfile.objects.filter(user=user).exists()
    has_doctor_profile = DoctorProfile.objects.filter(user=user).exists()

    if has_patient_profile or has_doctor_profile:
        return HttpResponse("")  # Return an empty response if they have a profile

    # If neither profile exists, return a dialog with options to register
    return render(request, "health/profile_check_dialog.html")


@login_required
def add_doctor_profile(request):
    # Check if the doctor profile already exists
    try:
        doctor_profile = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        doctor_profile = None

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor_profile)
        if form.is_valid():
            doctor_profile = form.save(commit=False)
            doctor_profile.user = request.user  # Link to the logged-in user
            doctor_profile.save()
            return redirect('doctor_dashboard')  # Redirect after saving
    else:
        form = DoctorProfileForm(instance=doctor_profile)

    return render(request, 'health/add_doctor.html', {'form': form, 'title': 'Add or Update Doctor Profile'})


@login_required
def add_patient_profile(request):
    # Check if the patient profile already exists
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        patient_profile = None

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=patient_profile)
        if form.is_valid():
            patient_profile = form.save(commit=False)
            patient_profile.user = request.user  # Link to the logged-in user
            patient_profile.save()
            return redirect('patient_dashboard')  # Redirect after saving
    else:
        form = PatientProfileForm(instance=patient_profile)

    return render(request, 'health/add_patient.html', {'form': form, 'title': 'Add or Update Patient Profile'})


@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(DoctorProfile, user=request.user)

    # Fetch doctor's appointments and patients
    appointments = Appointment.objects.filter(doctor=doctor)
    # Fetch patients with health records and also those with appointments with the doctor
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


def add_medical_test(request):
    if request.method == 'POST':
        form = MedicalTestForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('doctor_dashboard')  
    else:
        form = MedicalTestForm()
    
    return render(request, 'health/add_medicaltest.html', {'form': form})

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(PatientProfile, id=patient_id)
    health_records = HealthRecord.objects.filter(patient=patient)
    medical_tests = MedicalTest.objects.filter(health_record__patient=patient)
    ai_predictions = AIModel.objects.filter(patient=patient).order_by('-id')[:2]

    context = {
        'patient': patient,
        'health_records': health_records,
        'medical_tests': medical_tests,
        'ai_predictions': ai_predictions
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
    patient = PatientProfile.objects.get(user=user)
    medical_records = HealthRecord.objects.filter(patient=patient)
    appointments = Appointment.objects.filter(patient=user)
    ai_predictions = AIModel.objects.filter(patient=patient).order_by('-id')[:2]
    # messages = Message.objects.filter(receiver=user)
    
    # Context to pass to template
    context = {
        'patient': patient,
        'medical_records': medical_records,
        'appointments': appointments,
        'ai_predictions': ai_predictions,
        # 'messages': messages,
    }
    return render(request, 'health/patientdashboard.html', context)


@require_POST
def describe_problem(request):
    # Get the problem description from the form
    user = request.user
    patient = PatientProfile.objects.get(user=user)
    medical_history = patient.medical_history
    problem_description = request.POST.get('problem_description')
    diseases = predict_disease(problem_description)
    doctors = predict_doctor(problem_description)
    try:
        insights = generate_insights(medical_history=medical_history, user_input=problem_description)
    except:
        insights = f"Find these doctors: {doctors}"
    print(diseases)
    print(doctors)
    print(insights)

    # Create an instance of AIModel with the problem description
    ai_model = AIModel(patient=patient, problem_description=problem_description, prognosis=diseases, recommended_doctor=doctors, ai_insights=insights)
    ai_model.save()
    


    # Show success message to the user
    messages.success(request, 'Your problem has been submitted and processed by AI.')

    # Redirect to the dashboard or any other page
    return redirect('patient_dashboard')


@login_required(login_url='authentication:login')
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
    
    return render(request, 'health/schedule_appointment.html', {'form': form})

def doctor_list(request):
    # Get all doctor profiles from the database
    doctors = DoctorProfile.objects.all()
    
    # Render the list in the template
    return render(request, 'health/doctor_list.html', {'doctors': doctors})

def home(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'health/home.html', {'doctors':doctors})

@login_required(login_url='authentication:login')
def logout_view(request):
    logout(request)
    return redirect('authentication:login')