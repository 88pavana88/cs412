# File: forms.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: Defines forms to create a new profile in Mini FB & add statuses to user profiles

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to create a new Profile.'''
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    profile_image_url = forms.URLField(label="Image URL", required=False)

    class Meta:
        '''Relates this form to the Profile model finalizes required and unrequired inputs.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Status message on a user's profile page.'''

    class Meta:
        '''relates this form to the StatusMessage model and finalizes required inputs'''
        model = StatusMessage
        fields = ['message'] 