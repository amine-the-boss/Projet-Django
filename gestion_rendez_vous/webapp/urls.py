from django.urls import path
from . import views

urlpatterns = [
    #path(route name, the view function, name same as the route)
    
    path('',views.home,name=""),
    
    path('register',views.register,name="register"),
    
    path('my-login',views.my_login,name="my-login"),
    
    path('user-logout',views.user_logout,name="user-logout"),
    
    path('add-patient',views.add_patient,name="add-patient"),
    
    path('update-patient/<int:pk>',views.update_patient,name="update-patient"),
    
    path('patient/<int:pk>', views.singular_patient, name="patient"),
    
    path('list-patient', views.list_patient, name="list-patient"),
    
    path('add-doctor',views.add_doctor,name="add-doctor"),
    
    path('list-doctor', views.list_doctor, name="list-doctor"),
    
    path('update-doctor/<int:pk>', views.update_doctor, name='update-doctor'),
    
    path('doctor/<int:pk>/', views.singular_doctor, name='doctor'),
    
    path('add-appointment',views.add_appointment,name="add-appointment"),
    
    path('list-appointment', views.list_appointment, name="list-appointment"),
    
    path('update-appointment/<int:pk>', views.update_appointment, name='update-appointment'),
    
    path('appointment/<int:pk>', views.singular_appointment, name="appointment"),
    
    path('calendar', views.calendar, name='calendar'),
    
    path('get_appointments', views.get_appointments, name='get-appointments'),
    
    path('get_user_appointments/', views.get_user_appointments, name='get_user_appointments'),
    
    path('resources/', views.list_resources, name='list-resources'),

    path('resources/add/', views.add_resource, name='add-resource'),
    
    path('resources/<int:pk>/update/', views.update_resource, name='update-resource'),
    
    path('resources/<int:pk>/', views.view_resource, name='view-resource'),
    
    
]