from django.db import models
from django.contrib.auth.models import User

class TripCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Trip categories"

class Trip(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    departure_date = models.DateTimeField()
    return_date = models.DateTimeField()
    departure_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    available_seats = models.IntegerField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='trips/')
    category = models.ForeignKey(TripCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    CLASS_CHOICES = [
        ('economic', 'Economic'),
        ('flexible', 'Flexible')
    ]
    travel_class = models.CharField(max_length=20, choices=CLASS_CHOICES, default='economic')
    economic_price = models.DecimalField(max_digits=10, decimal_places=2)
    flexible_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

    def is_available(self):
        return self.available_seats > 0

class TripOption(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.trip.name} - {self.name}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    number_of_persons = models.IntegerField()
    children_ages = models.JSONField(null=True, blank=True)
    selected_options = models.ManyToManyField(TripOption)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation {self.id} - {self.user.username} - {self.trip.name}"
