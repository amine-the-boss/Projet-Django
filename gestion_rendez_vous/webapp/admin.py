from django.contrib import admin

# Register your models here.

from . models import Patient

admin.site.register(Patient)


from .models import Doctor

admin.site.register(Doctor)

from .models import Appointment

admin.site.register(Appointment)

from .models import Resource

admin.site.register(Resource)
