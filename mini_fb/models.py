# File: models.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: The code in this file defines the Profile model, and specifies what data is needed for a user's profile
# Now we've also added the status message model for displaying user statuses

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of a FB Profile.'''

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    profile_image_url = models.URLField(blank=True) 

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'

    def get_status_messages(self):
        '''Retrieve all status messages related to this profile, ordered by timestamp.'''
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')

    def get_absolute_url(self):
        '''Return the URL for viewing this profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})


class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message on Mini Facebook.'''
    
    timestamp = models.DateTimeField(auto_now_add=True)  
    message = models.TextField(blank=False)  # Status message 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Link to profile

    def __str__(self):
        '''Return a string representation of this StatusMessage.'''
        return f'Status by {self.profile.first_name} on {self.timestamp.strftime("%Y-%m-%d %H:%M")}'

    def get_absolute_url(self):
        '''Return the URL for viewing the associated profile.'''
        return reverse('show_profile', kwargs={'pk': self.profile.pk})