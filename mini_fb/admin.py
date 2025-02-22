# File: admin.py
# Author: Pavana Manoj (pavana@bu.edu), 02/22/2025
# Description: The code in this file allows users to register for Mini FB.

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)