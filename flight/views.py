from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .models import BookingModel, FlightDetails
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime, date
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

# Create your views here.


@login_required(login_url='login')
def home(request):
    news = "📢 Book Domestic and International Flight Tickets Here!!"

    query_from = request.GET.get('from', '').strip()
    query_to = request.GET.get('to', '').strip()

    flights = FlightDetails.objects.all()

    if query_from and query_to:
        flights = flights.filter(
            Q(flight_from__icontains=query_from) & Q(flight_to__icontains=query_to)
        )
    elif query_from:
        flights = flights.filter(flight_from__icontains=query_from)
    elif query_to:
        flights = flights.filter(flight_to__icontains=query_to)

    return render(request, 'home.html', {'flights': flights,'news': news})

@login_required(login_url='login')
def about_us(request):
    return render(request,'about_us.html')

def book_flight(request, id):
    flight = FlightDetails.objects.get(id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phno = request.POST.get("phno")
        age = request.POST.get("age")
        booking_date = request.POST.get("booking_date")


        booking=BookingModel.objects.create(
            flight_name=flight, 
            name=name,
            email=email,
            phno=phno,
            age=age,
            booking_date=booking_date
        )

        return redirect("payment",id=booking.id) 
    return render(request, 'booking.html', {'flight': flight})

@login_required(login_url='login')

def payment_view(request, id):
    booking = get_object_or_404(BookingModel, id=id)

    base_fare = booking.flight_name.flight_ticket_price
    surcharge = 100
    total_fare = base_fare + surcharge

    if request.method == "POST":
        # 👉 Normally you’d integrate Razorpay/Stripe, but here we simulate success
        card_number = request.POST.get("card_number")
        holder = request.POST.get("card_holder")
        expiry = request.POST.get("expiry")
        cvv = request.POST.get("cvv")

        if card_number and holder and expiry and cvv:  
            # Fake "payment successful"
            booking.is_paid = True
            booking.save()

            context = {
                "success": True,
                "ticket": booking,   # use booking object as "ticket"
                "total_fare": total_fare,
            }
            return render(request, "booking_list.html", context)
        else:
            # Payment failed (missing fields)
            return render(request, "booking_list.html", {"success": False})

    # GET → show form
    context = {
        "booking": booking,
        "total_fare": total_fare,
    }
    return render(request, "payment.html", context)


# def payment_view(request, id):
#     booking = BookingModel.objects.get(id=id)

#     base_fare = booking.flight_name.flight_ticket_price
#     surcharge = 100
#     total_fare = base_fare + surcharge

#     context = {
#         "booking": booking,
#         "total_fare": total_fare,
#     }
#     return render(request, "payment.html", context)


@login_required(login_url='login')
def booking_list(request):
    bookings = BookingModel.objects.exclude(status='Cancelled')

    for booking in bookings:
        base_fare = booking.flight_name.flight_ticket_price
        surcharge = 100
        booking.total_fare = base_fare + surcharge
    
    return render(request, 'booking_list.html', {'bookings': bookings})


def confirm_booking(request, id):
    booking = get_object_or_404(BookingModel, id=id)
    booking.status = 'Confirmed'
    booking.save()
    return redirect('booking_list')  

def cancel_booking(request, id):
    booking = get_object_or_404(BookingModel, id=id)
    booking.status = 'Cancelled'
    booking.save()
    return redirect('booking_list')

@login_required(login_url='login')
def booking_history(request):
    cancelled_bookings = BookingModel.objects.filter(status='Cancelled')
    return render(request, 'booking_history.html', {'cancelled_bookings': cancelled_bookings})

def update(request,pk):
    update_booking = BookingModel.objects.get(id=pk)
    
    print(update_booking.__dict__)

    if request.method == "POST":
        update_booking.name = request.POST.get("name")
        update_booking.email = request.POST.get("email")
        update_booking.phno = request.POST.get("phno")
        update_booking.age = request.POST.get("age")
        update_booking.booking_date = request.POST.get("booking_date")
        update_booking.save()
        return redirect('booking_list')

    return render(request, 'update.html', {
        'update_booking': update_booking
    })



