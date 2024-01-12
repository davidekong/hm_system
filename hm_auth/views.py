from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # Import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import HospitalPersonnel, Hospital, Patient

import datetime
from django.urls import reverse
# Create your views here.

def table(request):
    return render(request, 'hm_auth/table.html')

@login_required
def logout_user(request):
    # Log out the user
    logout(request)
    # Render the logout template
    return render(request, 'hm_auth/logout.html')

def logIn(request):
    logout(request)
    context = {
        'error_message': ''
    }
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = User.objects.get(email=email).username
        user = authenticate(username=username, password=password)
        if user is not None:
            print('logged')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('choose_add_account')
        else:
            context['error_message'] = "Did you put in the right credentials? Try registering"
    return render(request, 'hm_auth/login.html', context)



@login_required
def add_hospital(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST['name']
        address = request.POST['address']
        admin_id = request.POST['admin']
        admin = User.objects.get(pk=admin_id)
        license_data = 'license_data' in request.POST
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        website = request.POST['website']
        established_date = request.POST.get('established_date', None)
        description = request.POST['description']
        services = request.POST['services']
        specialties = request.POST['specialties']
        accreditation = request.POST['accreditation']
        image = request.FILES.get('image', None)

        # Create a new hospital instance
        new_hospital = Hospital(
            name=name,
            address=address,
            admin=admin,
            license_data=license_data,
            phone_number=phone_number,
            email=email,
            website=website,
            established_date=established_date,
            description=description,
            services=services,
            specialties=specialties,
            accreditation=accreditation,
            image=image
        )

        # Save the hospital instance
        new_hospital.save()

        # Display success message
        messages.success(request, 'Hospital added successfully!')

        # Redirect to a different page if needed
        return redirect('home')  # Change 'home' to the desired URL name

    return render(request, 'hospital_form.html')  # Replace 'hospital_form.html' with the actual template name

@login_required
def choose_add_account(request):
    context = {}

    if request.method == "POST":
        if 'add_patient' in request.POST:
            return redirect("add_patient")
        else:
            return redirect("add_personnel")

    # Check if the user is associated with a HospitalPersonnel
    user_associated = HospitalPersonnel.objects.filter(user=request.user).exists()
    patient_associated = Patient.objects.filter(user=request.user).exists()
    if user_associated:
        context['personnel'] = HospitalPersonnel.objects.filter(user=request.user)[0]
    if patient_associated:
        context['patient'] = Patient.objects.filter(user=request.user)[0]
    context['is_associated'] = user_associated
    context['hospitals'] = Hospital.objects.all()
    context['is_patients'] = patient_associated

    return render(request, 'hm_auth/choose_add_account.html', context)

@login_required
def add_patient(request):
    context = {

    }
    if request.method == 'POST':
        # Get data from the form
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


@login_required
def join_hospital(request):
    context = {}

    if request.method == 'POST':
        # Get data from the form
        hospital_id = request.POST['hospital']
        role = request.POST['role']

        # Assuming you have a model for Hospital and 'hospital_id' is the ID of the selected hospital
        hospital = Hospital.objects.get(pk=hospital_id)

        # Check if the user is already associated with a HospitalPersonnel
        existing_personnel = HospitalPersonnel.objects.filter(user=request.user, hospital=hospital).exists()

        if not existing_personnel:
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
            return redirect('home')
        else:
            # Display a message indicating that the user is already associated with a HospitalPersonnel
            messages.warning(request, 'You are already associated with a Hospital Personnel for this hospital.')

        # Update the context with a boolean indicating whether the user is associated
        context['is_associated'] = existing_personnel

    # Update the context with the list of available hospitals
    context['hospitals'] = Hospital.objects.all()

    # Pass the context into the render function
    return render(request, 'hm_auth/join_hospital.html', context)

@login_required
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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if first_name == '' or last_name == '' or email == '' or password1 == '' or password2 == '':
            valid = False
            context['error_message'] = 'Please ensure all fields are appropriately filled.'
        elif len(password1) < 5:
            valid = False
            context['error_message'] = 'Please ensure password is not less than 5 characters.'
        else:
            valid = True
        
        if valid == True:
            if password1 == password2:
                user = authenticate(email=email)
                if user is None:
                    new_user = User.objects.create_user(username=first_name+last_name, first_name=first_name, last_name=last_name, email=email, password=password1)

                    new_user.save()
                    login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('choose_add_account')
                else:
                    context['error_message'] = "This email is already in use. Would you like to login?"
            else:
                context['error_message'] = 'Please make sure both passwords match.'
    return render(request, 'hm_auth/signup.html', context)
