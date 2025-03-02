# File: forms.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: Defines forms to create a new profile in Mini FB.

from django import forms
from .models import Profile

class CreateProfileForm(forms.ModelForm):
    '''A form to create a new Profile.'''

    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    profile_image_url = forms.URLField(label="Image URL", required=False)

    class Meta:
        '''Relates this form to the Profile model.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
