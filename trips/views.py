from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Trip, TripOption, Reservation
from .forms import ReservationForm
import paypalrestsdk
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Reservation
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def trip_list(request):
    trips = Trip.objects.all()
    category = request.GET.get('category')
    if category:
        trips = trips.filter(category__name=category)
    return render(request, 'trips/trip_list.html', {'trips': trips})

def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    options = trip.options.all()
    return render(request, 'trips/trip_detail.html', {
        'trip': trip,
        'options': options
    })

@login_required
def make_reservation(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # Create reservation
        reservation = Reservation.objects.create(
            user=request.user,
            trip=trip,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            status='pending'
        )
        
        # Redirect to payment page
        return redirect('trips:payment_process', reservation_id=reservation.id)
        
    return render(request, 'trips/make_reservation.html', {
        'trip': trip
    })

@login_required
def payment_process(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'trips/payment.html', {
        'reservation': reservation,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    })

@require_POST
@login_required
def payment_complete(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.status = 'confirmed'
    reservation.save()
    return JsonResponse({'success': True})

@login_required
def payment_success(request):
    return render(request, 'trips/payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'trips/payment_cancel.html')
def payment_cancel(request):
    return render(request, 'trips/payment_cancel.html')
