# File: views.py
# Author: Pavana Manoj (pavana@bu.edu), 04/26/2025
# Description: defines views for services, appointments, reviews, and customer accounts in the nail salon app

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# used to combine the service detail view with the appointment booking form on the same page
from django.views.generic.edit import FormMixin
from django.views import View
# reverse_lazy is like reverse, but works better with class-based views cuz it waits to figure out the URL until it needs to
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Service, Customer, NailTechnician, Appointment, Review
from .forms import AppointmentForm, CreateCustomerForm, ReviewForm

# show list of services
class ServiceListView(ListView):
    '''shows list of available services'''
    model = Service
    template_name = "project/service_list.html"

# show service details and appointment form
class ServiceDetailView(FormMixin, DetailView):
    '''shows service details and form to book appointment'''
    model = Service
    template_name = "project/service_detail.html"
    form_class = AppointmentForm

    def get_success_url(self):
         return reverse("my_appointments")

    def get_form_kwargs(self):
        '''pass technician and date to form for time filtering'''
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            technician_id = self.request.POST.get("technician")
            date = self.request.POST.get("date")
            if technician_id and date:
                try:
                    technician = NailTechnician.objects.get(id=technician_id)
                    kwargs.update({'technician': technician, 'date': date})
                except NailTechnician.DoesNotExist:
                    pass
        return kwargs

    def get_context_data(self, **kwargs):
        '''add form to context'''
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        '''handle form submission to create appointment'''
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.service = self.object
            try:
                appointment.customer = Customer.objects.get(user=self.request.user)
            except Customer.DoesNotExist:
                return redirect("create_customer")
            appointment.save()
            return self.form_valid(form)
        return self.form_invalid(form)

# register user and create customer profile
class RegisterAndCreateCustomerView(CreateView):
    '''register a new user and create a customer profile'''
    template_name = "project/register_and_create_customer.html"
    success_url = reverse_lazy("service_list")
    form_class = CreateCustomerForm

    def get_context_data(self, **kwargs):
        '''add user and customer forms to context'''
        context = super().get_context_data(**kwargs)
        context["user_form"] = kwargs.get("user_form", UserCreationForm())
        context["customer_form"] = kwargs.get("customer_form", CreateCustomerForm())
        return context

    def post(self, request, *args, **kwargs):
        '''handle user and customer form submission'''
        self.object = None
        user_form = UserCreationForm(request.POST)
        customer_form = CreateCustomerForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(
            user_form=user_form,
            customer_form=customer_form
        ))

# create new appointment
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    '''create a new appointment'''
    model = Appointment
    form_class = AppointmentForm
    template_name = "project/appointment_form.html"
    success_url = reverse_lazy("service_list")

    def form_valid(self, form):
        '''set customer and status before saving'''
        customer = get_object_or_404(Customer, user=self.request.user)
        form.instance.customer = customer
        form.instance.status = "scheduled"
        return super().form_valid(form)

# list appointments for user or all for admin
class MyAppointmentsView(LoginRequiredMixin, ListView):
    '''list appointments for current user or all customer appointments for admin'''
    model = Appointment
    template_name = "project/my_appointments.html"
    context_object_name = "appointments"

    def get_queryset(self):
        '''return appointments for user or all for admin'''
        if self.request.user.is_superuser:
            return Appointment.objects.all().order_by('date', 'time')
        customer = get_object_or_404(Customer, user=self.request.user)
        return Appointment.objects.filter(customer=customer).order_by('date', 'time')

# cancel appointment
class CancelAppointmentView(LoginRequiredMixin, View):
    '''cancel an appointment'''
    def post(self, request, pk):
        if request.user.is_superuser:
            appointment = get_object_or_404(Appointment, pk=pk)
        else:
            customer = get_object_or_404(Customer, user=request.user)
            appointment = get_object_or_404(Appointment, pk=pk, customer=customer)
        appointment.status = "cancelled"
        appointment.save()
        return redirect('my_appointments')

# mark appointment as completed
class CompleteAppointmentView(LoginRequiredMixin, View):
    '''admin can mark an appointment as completed'''
    def post(self, request, pk):
        if not request.user.is_superuser:
            return redirect("service_list")
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.status = "completed"
        appointment.save()
        return redirect("my_appointments")

# create review for completed appointment
class CreateReviewView(LoginRequiredMixin, CreateView):
    '''create a review for a completed appointment'''
    model = Review
    form_class = ReviewForm
    template_name = "project/create_review.html"

    def dispatch(self, request, *args, **kwargs):
        self.appointment = get_object_or_404(
            Appointment, 
            pk=self.kwargs['pk'], 
            customer__user=request.user, 
            status='completed'
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        '''link review to customer, technician, and appointment'''
        form.instance.customer = self.appointment.customer
        form.instance.technician = self.appointment.technician
        form.instance.appointment = self.appointment
        return super().form_valid(form)

    def get_success_url(self):
        '''redirect to my appointments after submitting review'''
        return reverse("my_appointments")

# show all reviews
class ReviewListView(ListView):
    '''show all customer reviews'''
    model = Review
    template_name = "project/reviews.html"
    context_object_name = "reviews"
    
    def get_context_data(self, **kwargs):
        '''adds ratings to context for the filter form'''
        context = super().get_context_data(**kwargs)
        context['ratings'] = range(1, 6)
        return context

    def get_queryset(self):
        '''filters reviews by star rating'''
        queryset = super().get_queryset().order_by('-timestamp')
        selected_rating = self.request.GET.get('rating')
        if selected_rating:
            queryset = queryset.filter(rating=selected_rating)
        return queryset

# update review by customer
class UpdateReviewView(LoginRequiredMixin, UpdateView):
    '''update a review created by the customer'''
    model = Review
    form_class = ReviewForm
    template_name = "project/update_review_form.html"

    def get_object(self):
        '''only allow review owner to update'''
        return get_object_or_404(Review, pk=self.kwargs['pk'], customer__user=self.request.user)

    def get_success_url(self):
        '''redirect to my appointments after updating review'''
        return reverse('my_appointments')

# delete review by customer
class DeleteReviewView(LoginRequiredMixin, DeleteView):
    '''delete a review created by the customer'''
    model = Review
    template_name = "project/delete_review_form.html"
    context_object_name = "review"

    def get_object(self):
        '''only allow review owner to delete'''
        return get_object_or_404(Review, pk=self.kwargs['pk'], customer__user=self.request.user)

    def get_success_url(self):
        '''redirect to my appointments after deleting review'''
        return reverse('my_appointments')
