# File: admin.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: The code in this file allows users to use new features added to Mini FB via admin

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, Image, StatusImage, Friend
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image) #New
admin.site.register(StatusImage) #New
admin.site.register(Friend) #New