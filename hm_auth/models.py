from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital_admin')
    license_data = models.BooleanField(default=False)  # Indicates whether the hospital has licensed data for research
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    services = models.TextField(blank=True, null=True)  # A description of the services provided by the hospital
    specialties = models.TextField(blank=True, null=True)  # Specialties or focus areas of the hospital
    accreditation = models.CharField(max_length=100, blank=True, null=True)  # Accreditation details
    image = models.ImageField(upload_to='hospital_images/', blank=True, null=True)  # Image representing the hospital
    # Add more fields as needed

    def __str__(self):
        return self.name

class HospitalPersonnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)  # Doctor, Nurse, etc.
    is_admin = models.BooleanField(default=False)  # Indicates whether the personnel is also an admin
    # Add more fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)  # Information about patient allergies
    image = models.ImageField(upload_to='patient_images/', blank=True, null=True)  # Image representing the patient
    # Add more fields as needed

    def __str__(self):
        return self.user.username

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    test_results = models.TextField(blank=True, null=True)
    ai_predictability_flag = models.BooleanField(default=False)  # "flow" or similar label
    # Add more fields for medical records

    def __str__(self):
        return f"Record for {self.patient.user.username} at {self.hospital.name}"
