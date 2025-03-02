# File: views.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: The code in this file defines what is displayed when viewing all existing profiles at once and individual profiles
# Now including creating a profile pages's view and adding a status message page's view.

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm


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

class CreateProfileView(CreateView):
    '''Creates new Profile object.'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self):
        '''Goes to new profile page after submission.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(CreateView):
    '''Creates a new StatusMessage.'''
    
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        '''Add the Profile object to the template context.'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Attach the Profile foreign key before saving.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile  
        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the profile page after submission.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
