# File: urls.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: Sets URLs for page displaying all profiles and a page for displaying individual profiles
# Now include URL to page where you can add a user status to a user's profile too

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView

urlpatterns = [
    path("", ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"), # NEW for creating new profile page
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"), # NEW for adding a status message to a user's profile page
]
