from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Patient(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
        ('O', 'Other')
    )
    
    first_name = models.CharField(max_length=100)
    
    last_name = models.CharField(max_length=100)
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    date_of_birth = models.DateField()
    
    address = models.CharField(max_length=255)
    
    city = models.CharField(max_length=100)
    
    zip_code = models.CharField(max_length=20)
    
    phone_number = models.CharField(max_length=20)
    
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"






class Doctor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    SPECIALTY_CHOICES = (
    ('GP', 'General Practitioner'),
    ('SP', 'Specialist'),
    ('SUR', 'Surgeon'),
    ('OPHT', 'ophthalmologist'),
    ('OBGYN', 'Obstetrician/Gynecologist'),
    ('PED', 'Pediatrician'),
    ('ORTHO', 'Orthopedic Surgeon'),
    ('CARD', 'Cardiologist'),
    ('DERM', 'Dermatologist'),
    ('ENT', 'Otolaryngologist (ENT)'),
    ('NEURO', 'Neurologist'),
    ('PSY', 'Psychiatrist'),
    ('URO', 'Urologist'),
    
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=5, choices=SPECIALTY_CHOICES)
    gender = models.CharField(max_length=1, choices=Patient.GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=1, choices=Patient.MARITAL_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
    
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
        ('Rescheduled', 'Rescheduled'),
        ('Pending', 'Pending'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField(help_text='YYYY-MM-DD format')  # Define the date format
    appointment_time = models.TimeField(help_text='HH:MM format')  # Define the start time format
    end_time = models.TimeField(help_text='HH:MM format', blank=True, null=True) 
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.patient} at {self.appointment_date} {self.appointment_time}"



class Resource(models.Model):
    STATES = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('out_of_stock', 'Out of Stock'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    state = models.CharField(max_length=20, choices=STATES, default='available')

    def __str__(self):
        return self.name