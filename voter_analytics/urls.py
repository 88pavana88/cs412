# File: urls.py
# Author: Pavana Manoj (pavana@bu.edu), 04/06/2025
# Description: urls to views for the voter analytics

from django.urls import path
from . import views
from .views import VoterListView, VoterDetailView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'), #initial form and all voters 
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'), #individual voter page
]
 