"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# File: urls.py
# Author: Pavana Manoj (pavana@bu.edu), 03/01/2025
# Description: The code sets the urls for each app


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mini_fb.urls")), # put restaurant's url first to make it route automatically to its homepage instead of quotes'
    path("quotes/", include("quotes.urls")),
    path("mini_fb/", include("mini_fb.urls")), # new for mini fb
    
]
