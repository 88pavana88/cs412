# File: views.py
# Author: Pavana Manoj (pavana@bu.edu), 02/22/2025
# Description: The code in this file defines what is displayed when viewing all existing profiles at once and individual profiles

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Profile

class ShowAllProfilesView(ListView):
    '''Shows all of the existing user profiles.'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    '''Shows an individual profile.'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"
