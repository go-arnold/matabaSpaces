from django.db import models
from django.utils import timezone
from park.models import ParkingArea, Slot
from authentication.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_area = models.ForeignKey(ParkingArea, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    

    def __str__(self):
        return f'Reservation {self.id} by {self.user}'

