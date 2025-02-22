# File: models.py
# Author: Pavana Manoj (pavana@bu.edu), 02/22/2025
# Description: The code in this file defines the Profile model, and specifies what data is needed for a user's profile

from django.db import models

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
