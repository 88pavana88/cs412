# File: models.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: The code in this file defines the Profile model, and specifies what data is needed for a user's profile
# Now we've also added the status message model for displaying user statuses
# Also added the image and statusimage models for uploading and linking images to statuses
# Also added the friend model for modeling friendships between user profiles
# Includes methods for getting friends, adding friends, suggesting friends, and viewing a news feed

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of a FB Profile.'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    profile_image_url = models.URLField(blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #new

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'

    def get_status_messages(self):
        '''Retrieve all status messages related to this profile, ordered by timestamp.'''
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')

    def get_absolute_url(self):
        '''Return the URL for viewing this profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        '''Return a list of users that are friends with this user.'''
        friendships = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friends = []
        #goes through each friend of a user
        for f in friendships:
            if f.profile1 == self:
                friends.append(f.profile2)
            else:
                friends.append(f.profile1)
        return friends
    
    def add_friend(self, other):
        '''Adds a friendship between current user and another user.'''
        # doesn't allowing friending oneself
        if self == other:
            return
        
        # check if already friends to prevent duplicate friendships
        existing = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) |
            models.Q(profile1=other, profile2=self)
        )
        if not existing.exists():
            friendship = Friend(profile1=self, profile2=other)
            friendship.save()

    def get_friend_suggestions(self):
        # retrieve all friends
        friends = self.get_friends()
        friends_ids = [friend.pk for friend in friends]
        friends_ids.append(self.pk)

        # shows friend suggestions if not friends already
        return Profile.objects.exclude(pk__in=friends_ids)
    
    def get_news_feed(self):
        '''Return a list of StatusMessages from this profile and its friends, ordered by timestamp descending.'''
        # get friends
        friends = self.get_friends()
        
        # include self and friends
        profiles = [self] + list(friends)
        
        # get status messages from these profiles
        return StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')


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

    def get_images(self):
        '''Return all images related to this status message.'''
        return Image.objects.filter(statusimage__status_message=self)

    
class Image(models.Model):
    '''Represents an image uploaded by a user.'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded by {self.profile.first_name} {self.profile.last_name} at {self.timestamp}"


class StatusImage(models.Model):
    '''Links an image to a specific status message.'''
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    image = models.ForeignKey("Image", on_delete=models.CASCADE)

    def __str__(self):
        return f"Image linked to StatusMessage {self.status_message.pk}"
    
class Friend(models.Model):
    '''Encapsulates the idea of a friendship between to people (profiles) on MiniFB & the date they became friends'''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
