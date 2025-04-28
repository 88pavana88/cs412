# File: forms.py
# Author: Pavana Manoj (pavana@bu.edu), 04/23/2025
# Description: Defines forms to create and manage customer accounts, appointments, and reviews for the Nail Salon app.

from django import forms
from .models import Appointment, TIME_CHOICES, Customer, Review

class AppointmentForm(forms.ModelForm):
    '''a form to create an appointment and dynamically filter available times'''
    class Meta:
        '''relates this form to the Appointment model and hides customer, status, and service fields'''
        model = Appointment
        # exclude both customer and status so neither appears in the form
        exclude = ['customer', 'status', 'service']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # calendar picker
        }

    def __init__(self, *args, **kwargs):
        '''initialize form and limit time choices based on technician and date'''
        # get the technician and date passed from the view
        technician = kwargs.pop('technician', None)
        date = kwargs.pop('date', None)

        # call the parent constructor
        super().__init__(*args, **kwargs)

        # dynamically filter available times based on technician and date
        if technician and date:
            booked_times = Appointment.objects.filter(
                technician=technician, date=date
            ).values_list('time', flat=True)

            # only show available time slots
            self.fields['time'].choices = [
                (time, label) for time, label in TIME_CHOICES if time not in booked_times
            ]
            
class CreateCustomerForm(forms.ModelForm):
    '''a form to collect customer info including name, email, and phone'''
    class Meta:
        '''relates this form to the Customer model and includes all contact fields'''
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number']

class ReviewForm(forms.ModelForm):
    '''a form to submit a star rating and review for a service'''
    class Meta:
        '''relates this form to the Review model and defines rating and comment inputs'''
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
            'rating': forms.Select(choices=[(i, f"{i} stars") for i in range(1, 6)]),
        }

