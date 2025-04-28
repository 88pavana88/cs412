# File: urls.py
# Author: Pavana Manoj (pavana@bu.edu), 04/23/2025
# Description: URL configuration for the nail salon app

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterAndCreateCustomerView, CancelAppointmentView, CompleteAppointmentView, CreateReviewView, ReviewListView, UpdateReviewView, DeleteReviewView

urlpatterns = [
    path("", views.ServiceListView.as_view(), name="service_list"),
    path("service/<int:pk>/", views.ServiceDetailView.as_view(), name="service_detail"),
    path("login/", auth_views.LoginView.as_view(template_name="project/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="service_list"), name="logout"),
    path("register/", RegisterAndCreateCustomerView.as_view(), name="register"),
    path("my_appointments/", views.MyAppointmentsView.as_view(), name="my_appointments"),
    path("appointments/cancel/<int:pk>/", CancelAppointmentView.as_view(), name="cancel_appointment"),
    path("appointments/complete/<int:pk>/", CompleteAppointmentView.as_view(), name="complete_appointment"),    
    path("appointments/<int:pk>/review/", CreateReviewView.as_view(), name="create_review"),
    path("reviews/", ReviewListView.as_view(), name="reviews"),
    path("reviews/<int:pk>/edit/", views.UpdateReviewView.as_view(), name="edit_review"),
    path("reviews/<int:pk>/delete/", views.DeleteReviewView.as_view(), name="delete_review"),

]

