from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Hospital, Doctor, Patient
from .forms import (
    DoctorRegistrationForm,
    PatientRegistrationForm,
    PrescriptionForm,
)
from .forms import DoctorForm, PatientForm


def home(request):
    hospitals = Hospital.objects.all()
    # show account registration forms on the homepage
    doctor_reg_form = DoctorRegistrationForm()
    patient_reg_form = PatientRegistrationForm()
    return render(request, 'hospital/home.html', {
        'hospitals': hospitals,
        'doctor_reg_form': doctor_reg_form,
        'patient_reg_form': patient_reg_form,
    })


def about(request):
    return render(request, 'hospital/about.html')


def contact(request):
    return render(request, 'hospital/contact.html')


def hospital_detail(request, pk):
    """Show a single hospital's details (database-backed)."""
    hospital = get_object_or_404(Hospital, pk=pk)
    return render(request, 'hospital/detail.html', {'hospital': hospital})


def register_doctor(request):
    # Render a registration page on GET; on POST create User+Doctor or re-render with errors
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            # create user
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                # create doctor profile
                Doctor.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    email=email,
                    phone_number=form.cleaned_data['phone_number'],
                    specialization=form.cleaned_data.get('specialization', ''),
                    hospital=form.cleaned_data['hospital']
                )
                messages.success(request, 'Doctor account created. You can now log in.')
                return redirect('login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'hospital/register_doctor.html', {'form': form})


def register_patient(request):
    # Render a registration page on GET; on POST create User+Patient or re-render with errors
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                Patient.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    email=email,
                    phone_number=form.cleaned_data['phone_number'],
                    hospital=form.cleaned_data['hospital'],
                )
                messages.success(request, 'Patient account created. You can now log in.')
                return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'hospital/register_patient.html', {'form': form})


@login_required
def doctor_dashboard(request):
    # only allow users who have a doctor profile
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Access denied: not a doctor account.')
        return redirect('home')

    # Provide a prescription form limited to patients of the same hospital
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        form.fields['patient'].queryset = Patient.objects.filter(hospital=doctor.hospital)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = doctor
            prescription.save()
            messages.success(request, 'Prescription created.')
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
        form.fields['patient'].queryset = Patient.objects.filter(hospital=doctor.hospital)

    prescriptions = doctor.prescriptions.all()
    return render(request, 'hospital/doctor_dashboard.html', {'doctor': doctor, 'form': form, 'prescriptions': prescriptions})


@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, 'Access denied: not a patient account.')
        return redirect('home')

    prescriptions = patient.prescriptions.all()
    return render(request, 'hospital/patient_dashboard.html', {'patient': patient, 'prescriptions': prescriptions})


@login_required
def dashboard_redirect(request):
    """Redirect logged-in users to the appropriate dashboard based on their profile."""
    user = request.user
    if hasattr(user, 'doctor'):
        return redirect('doctor_dashboard')
    if hasattr(user, 'patient'):
        return redirect('patient_dashboard')
    messages.error(request, 'No dashboard available for your account.')
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    # show doctor or patient profile
    if hasattr(user, 'doctor'):
        profile = user.doctor
        return render(request, 'hospital/doctor_profile.html', {'doctor': profile})
    if hasattr(user, 'patient'):
        profile = user.patient
        return render(request, 'hospital/patient_profile.html', {'patient': profile})
    messages.error(request, 'No profile available for your account.')
    return redirect('home')


@login_required
def profile_edit(request):
    user = request.user
    if hasattr(user, 'doctor'):
        doctor = user.doctor
        if request.method == 'POST':
            form = DoctorForm(request.POST, instance=doctor)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated.')
                return redirect('profile')
        else:
            form = DoctorForm(instance=doctor)
        return render(request, 'hospital/edit_doctor_profile.html', {'form': form})

    if hasattr(user, 'patient'):
        patient = user.patient
        if request.method == 'POST':
            form = PatientForm(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated.')
                return redirect('profile')
        else:
            form = PatientForm(instance=patient)
        return render(request, 'hospital/edit_patient_profile.html', {'form': form})

    messages.error(request, 'No profile to edit.')
    return redirect('home')

