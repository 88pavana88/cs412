# File: views.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: Defines views for profiles, status messages, friendships, and authentication in Mini FB.

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm

# I used get_object_or_404 throughout based on a suggestion from ChatGPT.com because it said it's safer and avoids errors
# when fetching the logged-in user's Profile without relying on pk in the URL.

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm(self.request.POST or None)
        return context

    def form_valid(self, form):
        '''Creates user, logs them in, and links them to the profile.'''
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        '''Goes to new profile page after submission.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''Creates a new StatusMessage.'''
    login_url = 'login'
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        '''Add the Profile object to the template context.'''
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(Profile, user=self.request.user)
        return context

    def form_valid(self, form):
        '''Attach the Profile foreign key, save image(s), and link to StatusMessage.'''
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile
        sm = form.save()

        for file in self.request.FILES.getlist('files'):
            image = Image(profile=profile, image_file=file)
            image.save()
            StatusImage.objects.create(status_message=sm, image=image)

        return super().form_valid(form)

    def get_success_url(self):
        '''Redirect to the profile page after submission.'''
        profile = get_object_or_404(Profile, user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''Update an existing profile.'''
    login_url = 'login'
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        '''Gets the profile for the logged-in user.'''
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        '''Redirects after update'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''Confirm deleting a status message.'''
    login_url = 'login'
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status"

    def get_success_url(self):
        '''Redirect back to the profile page after deleting status.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''Update existing status message.'''
    login_url = 'login'
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"

    def get_success_url(self):
        '''Redirect back to the profile page.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class AddFriendView(LoginRequiredMixin, View):
    '''Takes care of adding a friend to a profile.'''
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        '''Adds friend and redirect to the profile page.'''
        profile = get_object_or_404(Profile, user=request.user)
        other = get_object_or_404(Profile, pk=kwargs['other_pk'])
        profile.add_friend(other)
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''Lists suggested friends of a user.'''
    login_url = 'login'
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Gets the profile for the logged-in user.'''
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        '''Add friend suggestions to the template'''
        context = super().get_context_data(**kwargs)
        context['suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''Displays the news feed for a profile.'''
    login_url = 'login'
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_object(self):
        '''Gets the profile for the logged-in user.'''
        return get_object_or_404(Profile, user=self.request.user)
