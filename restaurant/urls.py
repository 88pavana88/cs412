from django.urls import path
from . import views  

urlpatterns = [
    path("", views.main, name="main"),  # path to home page
    path("order/", views.order, name="order"),  # path to order page
    path("confirmation/", views.confirmation, name="confirmation"),  # path to order confirmation page
]
