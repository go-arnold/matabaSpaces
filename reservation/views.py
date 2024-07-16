from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Reservation
from park.models import ParkingArea, Slot
from authentication.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .tasks import check_expired_reservations


@login_required(login_url='login')
def reserve_slot(request, pk):
    
    slot = get_object_or_404(Slot, id=pk)
    parking_area = slot.area
    
    if request.method == 'POST':
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=int(request.POST['hours']))
        price_per_hour = slot.price  # Utilisation de la propriété price
        total_price = int(request.POST.get('hours')) * price_per_hour
        
        if not slot.status or slot.is_booked:
            messages.error(request, 'Slot already occupied or booked')
            return redirect('parking', parking_area_id=parking_area.id)
        
        reservation = Reservation.objects.create(
            user=request.user,
            parking_area=parking_area,
            slot=slot,
            start_time=start_time,
            end_time=end_time,
            price=total_price,
            is_active=True,
        )
        
        slot.is_booked = True
        
        parking_area.occupancy -= 1
        parking_area.save()
        slot.save()

        send_reservation_email(reservation)
        messages.success(request, 'Reservation created successfully')
        return redirect('parking', parking_area_id=parking_area.id)
    
    
    context = {
        'slot': slot,
        'parking_area': parking_area,
        'price_per_hour': slot.price
    }
    return render(request, 'reservation/reserve.html', context)


@login_required(login_url='login')
def selectSlot(request,pk):
    slot = get_object_or_404(Slot, id=pk)
    parking_area = slot.area
    price_per_hour = slot.price  
    
    context = {
        'slot': slot,
        'parking_area': parking_area,
        'price_per_hour': price_per_hour
    }
    return render(request, 'reservation/reserve.html', context)


def send_reservation_email(reservation):
    email = EmailMessage(
        'Your Parking Reservation',
        f'Your reservation for slot {reservation.slot.slot_number} at {reservation.parking_area.name} has been confirmed.\n\nReservation Details:\n\nSlot: {reservation.slot.slot_number}\nStart Time: {reservation.start_time}\nEnd Time: {reservation.end_time}\nPrice: {reservation.price}',
        to=[reservation.user.email],
    )
    email.send()

@login_required(login_url='login')
def release_slot(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)

    if slot.is_booked:
        # Si le slot est réservé, gérer la réservation
        reservation = Reservation.objects.filter(slot=slot, is_active=True).first()
        if reservation:
            reservation.is_active = False
            reservation.end_time = timezone.now()
            reservation.save()

            occupied_duration = (reservation.end_time - reservation.start_time).total_seconds() / 3600
            total_amount = occupied_duration * reservation.price_per_hour

            reservation.total_amount = total_amount
            reservation.save()

            send_billing_email(reservation)
        else:
            # Si pas de réservation trouvée, envoyer un email de remerciement à l'utilisateur occupant
            send_thank_you_email(slot.occupied_by, slot)

        slot.is_booked = False
        slot.occupied_by = None
        slot.save()

        messages.success(request, 'Slot released successfully.')

    return redirect('home')

def send_billing_email(reservation):
    email = EmailMessage(
        'Billing Information for Your Parking Reservation',
        f'Your parking reservation for slot {reservation.slot.slot_number} at {reservation.parking_area.name} has been billed.\n\nBilling Details:\n\nSlot: {reservation.slot.slot_number}\nStart Time: {reservation.start_time}\nEnd Time: {reservation.end_time}\nPrice per hour: {reservation.price_per_hour}\nTotal amount: {reservation.total_amount}',
        to=[reservation.user.email],
    )
    email.send()

def send_thank_you_email(user, slot):
    if user:
        email = EmailMessage(
            'Thank You for Using Our Parking Service',
            f'Dear {user.first_name},\n\nThank you for using our parking service at {slot.area.name}. We hope you had a great experience. If you have any feedback or questions, please feel free to contact us.\n\nBest regards,\nThe Parking Team',
            to=[user.email],
        )
        email.send()