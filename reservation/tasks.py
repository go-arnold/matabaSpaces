from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone
from .models import Reservation
from park.models import Slot
from celery import Celery
from celery.schedules import crontab

# Cette tâche vérifie les réservations expirées.
@shared_task
def check_expired_reservations():
    
    reservations = Reservation.objects.filter(is_active=True)
    
    for reservation in reservations:
        
        elapsed_time = timezone.now() - reservation.start_time
        # Si le temps écoulé est supérieur à 20 minutes (1200 secondes) et que le slot est toujours réservé mais pas occupé
        if elapsed_time.total_seconds() > 125 and reservation.slot.status and reservation.slot.is_booked:
            # On annule la réservation
            reservation.is_active = False
            reservation.slot.is_booked = False
            reservation.slot.save()
            reservation.save()
            # On envoie un email de notification à l'utilisateur
            send_cancellation_email(reservation)

# Cette tâche envoie un email de notification pour l'annulation d'une réservation
def send_cancellation_email(reservation):
    email = EmailMessage(
        'Your Parking Reservation has been cancelled',
        f'Your reservation for slot {reservation.slot.slot_number} at {reservation.parking_area.name} has been cancelled due to inactivity.\n\nReservation Details:\n\nSlot: {reservation.slot.slot_number}\nStart Time: {reservation.start_time}\nPrice: {reservation.price}',
        
        to=[reservation.user.email],
    )
    email.send()


app = Celery('matabaspaces')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Appelle `check_expired_reservations` toutes les 10 minutes
    sender.add_periodic_task(120.0, check_expired_reservations.s(), name='check reservations every 10 mins')
