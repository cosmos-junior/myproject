from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Patient, Prescription, Hospital


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'email', 'phone_number', 'specialization', 'hospital']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'aria-label': fname})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone_number', 'hospital', 'medical_record']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'aria-label': fname})


class DoctorRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    specialization = forms.CharField(max_length=255, required=False)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname, field in self.fields.items():
            # password uses PasswordInput but still gets form-control
            field.widget.attrs.update({'class': 'form-control', 'aria-label': fname})


class PatientRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'aria-label': fname})


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'aria-label': fname})
