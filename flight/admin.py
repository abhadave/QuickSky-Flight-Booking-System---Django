from django.contrib import admin
from .models import FlightDetails,BookingModel
# Register your models here.

class FlightDetailsAdmin(admin.ModelAdmin):
    list_display=['id','flight_company','flight_name','flight_number','flight_from','flight_to','flight_departure_time','flight_date','flight_ticket_price']
    ordering=['id']
    list_display_links=['flight_name']

admin.site.register(FlightDetails,FlightDetailsAdmin)


@admin.register(BookingModel)
class BookingModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phno",
        "age",
        "flight_name",
        "status",
        "booking_date",
    )
    list_filter = ("status", "booking_date", "flight_name")
    search_fields = ("name", "email", "phno")
    ordering = ("-booking_date",)