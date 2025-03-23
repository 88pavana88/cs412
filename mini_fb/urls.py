# File: urls.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: Sets URLs for page displaying all profiles and a page for displaying individual profiles
# Now include URL to page where you can add a user status to a user's profile too

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView, AddFriendView, ShowFriendSuggestionsView, ShowNewsFeedView

urlpatterns = [
    path("", ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"), # NEW for creating new profile page
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"), # NEW for adding a status message to a user's profile page
    path("profile/<int:pk>/update", UpdateProfileView.as_view(), name="update_profile"), #updating profiles
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),#to delete status message
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'), #to update status message
    path('profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'), #add friend
    path('profile/<int:pk>/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'), #suggested friends
    path("profile/<int:pk>/news_feed", ShowNewsFeedView.as_view(), name="news_feed"), #for news feed
]
