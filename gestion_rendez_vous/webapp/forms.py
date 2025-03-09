from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput,TextInput
from .models import Patient

#Creation d'un utilisateur

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        
#Connexion de l'utilisateur

class loginForm(AuthenticationForm):
    username=forms.CharField(widget=TextInput())
    password=forms.CharField(widget=PasswordInput())
    
    
#########add a patient#########

class AddPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'address', 'city', 'zip_code', 'phone_number', 'marital_status', 'emergency_contact_name', 'emergency_contact_phone']

        # Define the __init__ method of the AddPatientForm class
    def __init__(self, *args, **kwargs):
    # Call the __init__ method of the superclass (parent class) of AddPatientForm
        super(AddPatientForm, self).__init__(*args, **kwargs)
    
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
 

#######update a patient##########


# Define the UpdatePatientForm class, which inherits from forms.ModelForm
class UpdatePatientForm(forms.ModelForm):
    # Define the Meta class to provide metadata for the form
    class Meta:
        # Specify the model to use for the form
        model = Patient
        # Define the fields of the form based on the Patient model
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'address', 'city', 'zip_code', 'phone_number', 'marital_status', 'emergency_contact_name', 'emergency_contact_phone']

    def __init__(self, *args, **kwargs):
        
        super(UpdatePatientForm, self).__init__(*args, **kwargs)
        
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
        
        ##################DOCTOR###########################
        
from .models import Doctor

class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialty', 'gender', 'date_of_birth', 'address', 'phone_number', 'marital_status']  # Add more fields as needed

    def __init__(self, *args, **kwargs):
        super(AddDoctorForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})

class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialty', 'gender', 'date_of_birth', 'address', 'phone_number', 'marital_status']  # Add more fields as needed

    def __init__(self, *args, **kwargs):
        super(UpdateDoctorForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
        
        
##############################Resource##############################

from .models import Resource

class AddResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description', 'quantity', 'state']

class UpdateResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description', 'quantity', 'state']
        
        ##################APPOINTMENT###########################
from .models import Appointment

class AddAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'end_time' , 'appointment_time', 'reason', 'status', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(user_id=user)#to only get the patients of the loged in
        self.fields['doctor'].queryset = Doctor.objects.filter(user_id=user)#to only get the doctorss of the loged in
        

        
class UpdateAppointmentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UpdateAppointmentForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(user_id=user)#to only get the patients of the loged in
        self.fields['doctor'].queryset = Doctor.objects.filter(user_id=user)#to only get the doctorss of the loged in

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'end_time' , 'appointment_time', 'reason', 'status', 'notes']

        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
   
        
        
