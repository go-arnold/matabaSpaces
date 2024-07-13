from django.db import models
from authentication.models import User

# Create your models here.
class TheCity(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class ParkingArea(models.Model):
    
    name=models.CharField(max_length=100)
    city=models.ForeignKey(TheCity,on_delete=models.CASCADE,null=True,blank=True)
    esp_id=models.CharField(max_length=10)
    location = models.URLField(max_length=500)
    share_location=models.URLField(max_length=250)
    slots=models.IntegerField(default=0)
    occupancy=models.IntegerField(default=0)
    photo=models.ImageField(upload_to='parking_images/',default="images/parking.jpeg")
    workingtime=models.CharField(max_length=100, null=True)
    pricelvl1=models.IntegerField(null=True)       
    pricelvl2=models.IntegerField(null=True)       
    pricelvl3=models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Slot(models.Model):
    area = models.ForeignKey(ParkingArea, on_delete=models.CASCADE)
    occupied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slot_number = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    is_booked = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('area', 'slot_number')
    
    def get_slot_price(self):
        if self.slot_number % 3 == 1:
            return self.area.pricelvl1
        elif self.slot_number % 3 == 2:
            return self.area.pricelvl2
        else:
            return self.area.pricelvl3
        
    @property
    def price(self):
        return self.get_slot_price()
        
    def __str__(self):
        return str(self.slot_number)
    
  
    
class Platform(models.Model):
    leprix=models.CharField(max_length=200,null=True)
    startPrice=models.IntegerField(default=0)
    monthPrice=models.IntegerField(default=0)

    def __str__(self) :
        return str(self.leprix)
       


class FoundObject(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='found_objects/', default="images/avatar.png")
    date_found = models.DateField()
    parking_area = models.ForeignKey(ParkingArea, on_delete=models.CASCADE)   
    
    def __str__(self):
        return f"Found Object at {self.parking_area} - {self.description}"

class LostRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_area = models.CharField(max_length=100)
    date = models.DateField()
    photo = models.ImageField(upload_to='lost_requests/')
    description = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)  
    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return f"LostRequest from {self.user.username} at {self.parking_area} on {self.date}"
    
  

    
     