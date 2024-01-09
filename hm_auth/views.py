from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # Import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import HospitalPersonnel, Hospital, Patient

import datetime
from django.urls import reverse
# Create your views here.


def add_account(request):
    context = {

    }
    if request.method == "POST":
        if 'add_patient' in request.POST:
            return redirect("add_patient")
        else:
            return redirect("add_personnel")

    return render(request, 'hm_auth/add_account.html', context)

def add_patient(request):
    context = {

    }
    if request.method == 'POST':
        # Get data from the form
        username = request.POST['username']
        date_of_birth = request.POST.get('date_of_birth', None)
        gender = request.POST['gender']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        emergency_contact_name = request.POST['emergency_contact_name']
        emergency_contact_number = request.POST['emergency_contact_number']
        allergies = request.POST['allergies']
        image = request.FILES.get('image', None)

        # Create a new patient instance
        new_patient = Patient(
            user=request.user,  # Assuming the request.user is the logged-in user
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            phone_number=phone_number,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_number=emergency_contact_number,
            allergies=allergies,
            image=image
        )

        # Save the patient instance
        new_patient.save()

        # Display success message
        messages.success(request, 'Patient added successfully!')
        
        # Redirect to a different page if needed
        return redirect('home')
    return render(request, 'hm_auth/add_patient.html', context)

def add_personnel(request):
    context = {

    }
    if request.method == 'POST':
        # Get data from the form
        username = request.POST['username']
        hospital_id = request.POST['hospital']
        role = request.POST['role']

        # Assuming you have a model for Hospital and 'hospital_id' is the ID of the selected hospital
        hospital = Hospital.objects.get(pk=hospital_id)

        # Create a new hospital personnel instance
        new_personnel = HospitalPersonnel(
            user=request.user,  # Assuming the request.user is the logged-in user
            hospital=hospital,
            role=role,
            is_admin=False
        )

        # Save the hospital personnel instance
        new_personnel.save()

        # Display success message
        messages.success(request, 'Hospital Personnel added successfully!')

        # Redirect to a different page if needed
        return redirect('home')  # Change 'home' to the desired URL name

    # Assuming you have a variable 'hospitals' containing available hospitals
    hospitals = Hospital.objects.all()
    return render(request, 'hm_auth/add_personnel.html', {'hospitals': hospitals})

def home(request):
    context = {

    }

    return render(request, 'hm_auth/home.html', context)


def signup(request):
    context = {
        'error_message': ''
    }
    valid = False
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if username == '' or email == '' or password1 == '' or password2 == '':
            valid = False
            context['error_message'] = 'Please ensure all fields are appropriately filled.'
        elif len(password1) < 5:
            valid = False
            context['error_message'] = 'Please ensure password is not less than 5 characters.'
        else:
            valid = True
        
        if valid == True:
            if password1 == password2:
                user = authenticate(username=username, email=email)
                if user is None:
                    new_user = User.objects.create_user(username=username, email=email, password=password1)

                    new_user.save()
                    login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('add_account')
                else:
                    context['error_message'] = "There is already a user associated with the following credentials. Would you like to login?"
            else:
                context['error_message'] = 'Please make sure both passwords match.'
    return render(request, 'hm_auth/signup.html', context)
