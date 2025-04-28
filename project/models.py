# File: models.py
# Author: Pavana Manoj (pavana@bu.edu), 04/23/2025
# Description: Defines models for services, customers, appointments, technicians, and reviews in the Nail Salon app.

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# available time slots for appointments per day 
TIME_CHOICES = [
    ("09:00", "9:00 AM"),
    ("10:00", "10:00 AM"),
    ("11:00", "11:00 AM"),
    ("12:00", "12:00 PM"),
    ("13:00", "1:00 PM"),
    ("14:00", "2:00 PM"),
    ("15:00", "3:00 PM"),
    ("16:00", "4:00 PM"),
    ("17:00", "5:00 PM"),
    ("18:00", "6:00 PM"),
]

class Service(models.Model):
    '''Represents an offered nail salon service , including duration, price, and description.'''
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    '''Stores customer contact details including name, email, and phone number.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class NailTechnician(models.Model):
    '''Represents a nail technician with name, specialties, and optional availability notes.'''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    '''Links a customer, technician, and service to a specific date and time with an appointment status.'''
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    technician = models.ForeignKey(NailTechnician, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=5, choices=TIME_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=[
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled")
        ],
         default="scheduled"  # ensures "Scheduled" is used by default
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} at {self.time} with {self.technician}"

class Review(models.Model):
    '''Represents a customer review for a technician and appointment with a star rating.'''
    technician = models.ForeignKey(NailTechnician, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, f"{i} stars") for i in range(1, 6)])
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}/5 for {self.technician}"


