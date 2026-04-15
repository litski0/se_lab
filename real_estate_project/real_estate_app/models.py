from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    pincode_regex = RegexValidator(regex=r'^[1-9][0-9]{5}$', message="Please enter a valid 6-digit Indian pincode.")
    pincode = models.CharField(validators=[pincode_regex], max_length=6, blank=True)
    
    kyc_status = models.BooleanField(default=False)
    
    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Property(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Live', 'Live'),
        ('Booked', 'Booked'),
        ('Rejected', 'Rejected'),
    )
    property_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    address = models.TextField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='property_photos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.address} ({self.status})"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_photos/')

class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    )
    booking_id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    duration_months = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Booking {self.booking_id} for {self.property.address}"
