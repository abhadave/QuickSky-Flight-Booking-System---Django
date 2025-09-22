from django.db import models

# Create your models here.

class FlightDetails(models.Model):
    flight_company = models.CharField(max_length=100)
    flight_name = models.CharField(max_length=100)
    flight_number = models.IntegerField(default=0)
    flight_from = models.CharField(max_length=100)
    flight_to = models.CharField(max_length=100)
    flight_departure_time = models.TimeField()
    flight_date = models.DateField()
    flight_ticket_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.flight_name} ({self.flight_from} → {self.flight_to})"
    
class BookingModel(models.Model):
    flight_name = models.ForeignKey(FlightDetails, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=40)
    phno = models.CharField(max_length=10)
    age = models.IntegerField(default=0)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')


    def __str__(self):
        return f"{self.name} - {self.flight_name}"

