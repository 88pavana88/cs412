# File: admin.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: The code in this file allows users to use new features added to Mini FB

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage
admin.site.register(Profile)
admin.site.register(StatusMessage)