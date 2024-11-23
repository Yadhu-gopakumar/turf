from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import BookingSlotTable as BookingSlot
from .models import UserBookingTable as userBooking
from turfowner.models import turf_table
from django.utils import timezone
# Create your views here.
from django.contrib import messages

from datetime import datetime,time,timedelta



def bookslots(request, id):
    # Get the turf instance
    turf = get_object_or_404(turf_table, id=id)

    if request.method == "POST":
        # Get the selected slot IDs from the form (list of selected slot start times)
        selected_slots = request.POST.getlist("slot_ids[]")
        print("Selected slots:", selected_slots)
        booking_slot_table = BookingSlot.objects.filter(turf=turf, expired=False).first()

       
        if booking_slot_table:
            updated_slots = []  # This will store the updated slot data
            booked_slots = []  # This will store the booked slot details

            for slot in booking_slot_table.slots:

                # Check if the slot is selected and available
                if slot['start_time'] in selected_slots and slot['status'] == "available":
                    

                    # Update slot status to booked
                    slot['status'] = "booked"
                    slot['user']=request.user.username

                    # Create a dictionary for booked slots to be stored in userBooking
                    userslot_dict = {
                        'start_time': slot['start_time'],
                        'end_time': slot['end_time'],
                        'user':request.user.username,
                        'expired': False
                    }
                    booked_slots.append(userslot_dict)  # Add to booked slots

                updated_slots.append(slot)  # Add slot to updated list (whether booked or not)
           
            # Calculate the total amount based on the number of booked slots
            amount = len(booked_slots) * int(turf.rent)

            # Create a user booking record
            userBooking.objects.create(
                turfname=turf,
                customer=request.user,
                slots=booked_slots,
                amount=amount  # Adjust the amount if needed
            )

            # Save the updated slots back to the BookingSlotTable instance
            booking_slot_table.slots = updated_slots
            booking_slot_table.save()

            context = {
                'amount': amount
            }

            # Return a success response
            return render(request, 'bookingsuccess.html', context)



def userbookings(request):
    bookings=userBooking.objects.filter(customer=request.user).all()

    return render(request,'mybooking.html',{'bookings':bookings})



def cancelbooking(request, tid, bid):

    turf = get_object_or_404(turf_table, id=tid)
    booking_slot = get_object_or_404(BookingSlot, turf=turf, expired=False)
    userbook=userBooking.objects.get(id=bid)
    for i in userbook.slots:
        print(i['start_time'])

        for slots in booking_slot.slots:
             if slots['start_time']==i['start_time']:
                 slots['status']='available'
                 slots['user']=None
    turf.slots=True
    turf.save()             

    booking_slot.save()         
    userbook.delete()

    bookings=userBooking.objects.filter(customer=request.user).all()
  
    return render(request,'mybooking.html',{'bookings':bookings})
   