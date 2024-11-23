from django.contrib import admin
from .models import UserBookingTable,BookingSlotTable
# Register your models here.

admin.site.register(BookingSlotTable)
admin.site.register(UserBookingTable)