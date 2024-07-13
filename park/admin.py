from django.contrib import admin
from .models import ParkingArea,Slot,TheCity,Platform,FoundObject,LostRequest

# Register your models here.

admin.site.register(ParkingArea)
admin.site.register(Slot)

admin.site.register(TheCity)
admin.site.register(Platform)


admin.site.register(LostRequest)
admin.site.register(FoundObject)