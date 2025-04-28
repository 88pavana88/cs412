# File: admin.py
# Author: Pavana Manoj (pavana@bu.edu), 04/23/2025
# Description: registers nail salon models to admin panel

from django.contrib import admin
# Register your models here.
from .models import Service, Customer, NailTechnician, Appointment, Review

admin.site.register(Service)
admin.site.register(Customer)
admin.site.register(NailTechnician)
admin.site.register(Appointment)
admin.site.register(Review)
