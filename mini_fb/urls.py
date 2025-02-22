# File: urls.py
# Author: Pavana Manoj (pavana@bu.edu), 02/22/2025
# Description: Sets URLs for page displaying all profiles and a page for displaying individual profiles

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    path("", ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ShowProfilePageView.as_view(), name="show_profile"),
]
