# File: views.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: The code in this file defines what is displayed when viewing all existing profiles at once and individual profiles
# Now including creating a profile pages's view and adding a status message page's view.
# Now added views for updating/deleting profiles and status messages, adding friends, friend suggestions, and a newsfeed.

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, StatusMessage, Image, StatusImage
from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.shortcuts import redirect #ChatGPT.com informed me about this redirect function
from .models import Profile
from django.views import View

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
        '''Attach the Profile foreign key, save image(s), and link to StatusMessage.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile  

        # save the status message
        sm = form.save()

        # handle uploaded files
        files = self.request.FILES.getlist('files')
        for file in files:
            # create and save the Image object
            image = Image(profile=profile, image_file=file)
            image.save()

            # create and save the StatusImage relationship
            status_image = StatusImage(status_message=sm, image=image)
            status_image.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        '''Redirect to the profile page after submission.'''
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(UpdateView):
    '''Update an existing profile.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_success_url(self):
        '''Redirects after update'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class DeleteStatusMessageView(DeleteView):
    '''Confirm deleting a status message.'''
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status"

    def get_success_url(self):
        '''Redirect back to the profile page after deleting status.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    '''Update existing status message.'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"

    def get_success_url(self):
        '''Redirect back to the profile page.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class AddFriendView(View):
    '''Takes care of adding a friend to a profile.'''
    def dispatch(self, request, *args, **kwargs):
        '''Adds friend and redirect to the profile page.'''
        profile = Profile.objects.get(pk=kwargs['pk'])
        other = Profile.objects.get(pk=kwargs['other_pk'])
        profile.add_friend(other)
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    '''Lists suggested friends of a user.'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''Add friend suggestions to the template'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['suggestions'] = profile.get_friend_suggestions()
        return context

class ShowNewsFeedView(DetailView):
    '''Displays the news feed for a profile.'''
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"
