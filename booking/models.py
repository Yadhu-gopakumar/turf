from django.db import models

# Create your models here.
from turfowner.models import turf_table
from django.contrib.auth.models import User


import json
from datetime import time, timedelta

class BookingSlotTable(models.Model):
    turf = models.ForeignKey(turf_table, on_delete=models.CASCADE)
    booking_date = models.TimeField(auto_now_add=True)
    slots = models.JSONField(null=True,default=list)
    expired = models.BooleanField(default=False)



    class Meta:
        unique_together = ['turf', 'booking_date']
 

  


class UserBookingTable(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    turfname = models.ForeignKey(turf_table, on_delete=models.CASCADE)
    slots = models.JSONField(default=list,null=True)
    amount = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)  # Whether the booking is expired or not


    def __str__(self):
        return f"Booking by {self.customer} for {self.turfname} on {self.booking_date}"

