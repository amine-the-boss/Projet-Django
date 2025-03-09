from django.shortcuts import get_object_or_404, render, redirect
from .forms import AddAppointmentForm, CreateUserForm, UpdateAppointmentForm, loginForm, AddPatientForm,UpdatePatientForm
from django.http import JsonResponse 
from django.contrib.auth.models import auth#a function that will allow us to logout
from django.contrib.auth import authenticate#a function that will allow us to authentificate our user
from django.contrib.auth.decorators import login_required # will ensure that authentificqted have access to the right pages
from . models import Appointment, Patient
from .models import Doctor
from .forms import AddDoctorForm, UpdateDoctorForm

def home (request):
    #return HttpResponse('Hello World!')
    return render(request,'webapp/index.html')


#- sign up


def register(request):
    
    form=CreateUserForm()
    if request.method == "POST":
        
        form = CreateUserForm(request.POST)
        if form.is_valid():
                
            form.save()
            
            return redirect("my-login")
    
    context = {'form':form}
    
    return render(request,'webapp/register.html',context=context)
 
              

#---Login


def my_login(request):
    
    form = loginForm()
    
    if request.method == "POST":
        
        form = loginForm(request, data=request.POST)#sends a post request with all the data in our form
        if form.is_valid():
            
            username = request.POST.get('username')
            password = request.POST.get('password') 
            
            user = authenticate(request, username=username, password=password)  #check that the infos entered by the user are the same as in the bd 
                
            if user is not None:  #if the user exists
                auth.login(request, user)
                
                return redirect("calendar")   
    context = {'form':form}      
    return render(request,'webapp/my-login.html',context=context)


 # - Log out
 
 
@login_required(login_url='my-login')
def user_logout(request):
    
     auth.logout(request)
     
     return redirect("my-login")
 
 ###########################################################################################################################################
 
#-  List all the patients

@login_required(login_url='my-login')
def list_patient(request):
    my_patients = Patient.objects.filter(user_id=request.user)  # Filter patients belonging to the logged-in user
    context = {'patients': my_patients}
    return render(request, 'webapp/list-patient.html', context=context)


#-    Add a new patient
 
@login_required(login_url='my-login')
def add_patient(request):
    if request.method == 'POST':
        form = AddPatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user_id = request.user  # Assign the currently logged-in user
            patient.save()
            return redirect("list-patient")
    else:
        form = AddPatientForm()
    context = {'form': form}
    return render(request, 'webapp/add-patient.html', context=context)



#-    Update the patient's info

@login_required(login_url='my-login')
def update_patient(request, pk):
    # Retrieve the patient object based on the provided primary key (pk)
    patient = get_object_or_404(Patient, id=pk)
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = UpdatePatientForm(request.POST, instance=patient)
        # Check if the form is valid
        if form.is_valid():
            # Save the form and patient instance
            form.save()
            # Redirect to the dashboard or any other desired URL
            return redirect('list-patient')
    else:
        # If the request method is GET, create a form instance with the patient data
        form = UpdatePatientForm(instance=patient)
    
    # Render the update patient template with the form and patient data
    return render(request, 'webapp/update-patient.html', {'form': form})




#  -  view a single patient


@login_required(login_url='my-login')
def singular_patient(request, pk):

    all_patients = Patient.objects.get(id=pk)

    context = {'patient':all_patients}

    return render(request, 'webapp/view-patient.html', context=context)

###########################################DOCTOR#############################################################

#- List all the doctors


@login_required(login_url='my-login')
def list_doctor(request):
    my_doctors = Doctor.objects.filter(user_id=request.user)  # Filter doctors belonging to the logged-in user
    context = {'doctors': my_doctors}
    return render(request, 'webapp/list-doctor.html', context=context)

from .decorators import allowed_users

#-    Add a new doctor
@allowed_users(allowed_roles=['administrator'])
@login_required(login_url='my-login')
def add_doctor(request):
    if request.method == 'POST':
        form = AddDoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user  # Assign the currently logged-in user
            doctor.save()
            return redirect("list-doctor")
    else:
        form = AddDoctorForm()
    context = {'form': form}
    return render(request, 'webapp/add-doctor.html', context=context)



#-    Update the doctor's info


@allowed_users(allowed_roles=['administrator'])
@login_required(login_url='my-login')
def update_doctor(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    if request.method == 'POST':
        form = UpdateDoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('list-doctor')
    else:
        form = UpdateDoctorForm(instance=doctor)
    return render(request, 'webapp/update-doctor.html', {'form': form})



#  -  view a single doctor

@login_required(login_url='my-login')
def singular_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    context = {'doctor': doctor}
    return render(request, 'webapp/view-doctor.html', context=context)


############################Resource############################

from .models import Resource
from .forms import AddResourceForm, UpdateResourceForm

# List all resources
@login_required(login_url='my-login')
def list_resources(request):
    resources = Resource.objects.all()
    context = {'resources': resources}
    return render(request, 'webapp/list-resources.html', context=context)

# Add a new resource
@login_required(login_url='my-login')
def add_resource(request):
    if request.method == 'POST':
        form = AddResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list-resources")
    else:
        form = AddResourceForm()
    context = {'form': form}
    return render(request, 'webapp/add-resource.html', context=context)

# Update resource information
@login_required(login_url='my-login')
def update_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = UpdateResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect("list-resources")
    else:
        form = UpdateResourceForm(instance=resource)
    context = {'form': form}
    return render(request, 'webapp/update-resource.html', context=context)

# View a single resource
@login_required(login_url='my-login')
def view_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    context = {'resource': resource}
    return render(request, 'webapp/view-resource.html', context=context)

####################################Appointments############################


from django.contrib.auth.decorators import login_required
from .models import Patient  # Import the Patient model if you have one
from django.http import HttpResponse, HttpResponseForbidden



@login_required(login_url='my-login')
def list_appointment(request):
    my_appointments = Appointment.objects.filter(user_id=request.user)
    context = {'appointments': my_appointments}
    return render(request, 'webapp/list-appointment.html', context=context)






from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AddAppointmentForm

@login_required(login_url='my-login')
def add_appointment(request):
    if request.method == 'POST':
        form = AddAppointmentForm(request.user, request.POST)  # Pass request.user to the form
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect("list-appointment")
    else:
        form = AddAppointmentForm(request.user)  # Pass request.user to the form
    context = {'form': form}
    return render(request, 'webapp/add-appointment.html', context=context)




    


    
    
@login_required(login_url='my-login')
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)

    # Ensure that the appointment being updated belongs to the logged-in user
    if appointment.user != request.user:
        return HttpResponseForbidden("You don't have permission to update this appointment.")

    if request.method == 'POST':
        form = UpdateAppointmentForm(request.user, request.POST, instance=appointment)  # Pass request.user as the user argument
        if form.is_valid():
            form.save()
            return redirect('list-appointment')
    else:
        form = UpdateAppointmentForm(request.user, instance=appointment)  # Pass request.user as the user argument

    return render(request, 'webapp/update-appointment.html', {'form': form})


@login_required(login_url='my-login')
def singular_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    context = {'appointment': appointment}
    return render(request, 'webapp/view-appointment.html', context=context)

 


def get_appointments(request):
    appointments = Appointment.objects.all()
    events = []
    for appointment in appointments:
        events.append({
            'id': appointment.id, 
            'title': f"{appointment.patient.first_name} {appointment.patient.last_name}",
            'start': appointment.appointment_date.strftime('%Y-%m-%d') + 'T' + appointment.appointment_time.strftime('%H:%M:%S'),
            'end': appointment.appointment_date.strftime('%Y-%m-%d') + 'T' + appointment.end_time.strftime('%H:%M:%S') if appointment.end_time else None,
            'doctor': f"{appointment.doctor.first_name} {appointment.doctor.last_name}",
            'reason': appointment.reason,
            # Add other event properties as needed
        })
    print(events)  # Debugging: Print events to console
    return JsonResponse(events, safe=False)






def get_user_appointments(request):
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(user=request.user)
        events = []
    for appointment in appointments:
        events.append({
            'id': appointment.id, 
            'title': f"{appointment.patient.first_name} {appointment.patient.last_name}",
            'start': appointment.appointment_date.strftime('%Y-%m-%d') + 'T' + appointment.appointment_time.strftime('%H:%M:%S'),
            'end': appointment.appointment_date.strftime('%Y-%m-%d') + 'T' + appointment.end_time.strftime('%H:%M:%S') if appointment.end_time else None,
            'doctor': f"{appointment.doctor.first_name} {appointment.doctor.last_name}",
            'reason': appointment.reason,
            # Add other event properties as needed
        })
    print(events)  # Debugging: Print events to console
    return JsonResponse(events, safe=False)

    """ else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)"""
    
    
    
    


def calendar(request):
    return render(request, 'webapp/appointment_calendar.html')




