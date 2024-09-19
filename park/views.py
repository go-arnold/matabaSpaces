from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required,permission_required, user_passes_test
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import get_user_model
import json
from .models import ParkingArea,TheCity,Slot,FoundObject,LostRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from authentication.utils import is_member
from django.contrib import messages
from .models import ParkingArea
from django.db.models import Count
from django.db.models.functions import ExtractHour
from reservation.models import Reservation
from reservation.tasks import check_expired_reservations
from authentication.utils import is_member
from authentication.models import User


@csrf_exempt
def ldrdata(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            datas=data.items()
            print(datas)
            slots = 0
            occupancy = 0         

            esp_id = data.pop('esp_id')
            parking_area = ParkingArea.objects.get(esp_id=esp_id)            

            
            for slot_number, status in datas:
                if slot_number != 'esp_id':                 
                    slot_num = int(slot_number.replace('Slot',''))                
                    slot, created = Slot.objects.update_or_create(
                        area=parking_area,
                        slot_number=slot_num,
                        defaults={'status': status}
                )
                slots += 1
                if status and slot_number != 'esp_id':
                    occupancy += 1
                ParkingArea.objects.filter(id=parking_area.id).update(slots=slots, occupancy=occupancy)
        
            return JsonResponse({'success': 'Les donnees ont été enregistrees avec succes.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except ParkingArea.DoesNotExist:
            return JsonResponse({'error': 'ParkingArea non trouve.'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    

def home (request):     
    
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    
    parkings=ParkingArea.objects.filter(
        Q (city__name__icontains=q) |
        Q (location__icontains=q) |
        Q (name__icontains=q) 
    
    )
    #parkings=ParkingArea.objects.all() 
    parkingNum=parkings.count() 
    if parkingNum >1 :
        npark=parkingNum
        mpark=False
        ppark=False
    elif parkingNum ==1:
        mpark=parkingNum
        npark=False
        ppark=False
    else:
        ppark=parkingNum 
        mpark=False   
        npark=False    
    city=TheCity.objects.all()
    
    parks=ParkingArea.objects.all()
    for parking in parkings:
        slots = Slot.objects.filter(area=parking)
        total_slots = slots.count()
        available_slots = slots.filter(status=True, is_booked=False).count()
        parking.available_slots = available_slots
        parking.total_slots=total_slots
    
    context={'parkings':parkings,     
             'parks':parks,
             'cities':city,
             'npark':npark,
             'mpark':mpark,
             'ppark':ppark}
    return render(request,'home.html',context)

@login_required(login_url='login')
def parking(request, parking_area_id):
    parking = get_object_or_404(ParkingArea, id=parking_area_id)
    are_booked=Slot.objects.filter(area=parking, is_booked=True).count()
    slots = Slot.objects.filter(area=parking)
    libre=(parking.occupancy)-(are_booked)    
    
    total_slots = slots.count()
    
    slots_per_hour = slots.annotate(hour=ExtractHour('created_at')).values('hour').annotate(count=Count('id')).order_by('hour')
    
    occupancy_percentage = []
    for hour_data in slots_per_hour:
        hour = hour_data['hour']
        count = hour_data['count']
        percentage = (count / total_slots) * 100 if total_slots > 0 else 0
        occupancy_percentage.append({
            'hour': hour,
            'percentage': percentage
        })
    reservations=Reservation.objects.filter(parking_area=parking,user=request.user)
    is_parking_manager = is_member(request.user, 'ParkingManager')
    is_user = is_member(request.user, 'User')
    context = {
        
        'is_parking_manager':is_parking_manager,
        'is_user':is_user,
        'parking': parking,
        'occupancy_percentage': json.dumps(occupancy_percentage, cls=DjangoJSONEncoder),
        'slots':slots,
        'libre':libre,
        'reservations':reservations,
        'user':request.user,
    }
    
   
    return render(request, 'park/parking.html', context)

@login_required(login_url='login')
def pricing(request,pk):
    prices=ParkingArea.objects.get(id=pk)
    is_parking_manager = is_member(request.user, 'ParkingManager')
    is_user = is_member(request.user, 'User')
    context = {
        
        'is_parking_manager':is_parking_manager,
        'is_user':is_user,
        'prices':prices}
    return render(request,'park/pricing.html',context)


@login_required(login_url='login')
def occupy_slot(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)
    if slot.status and not slot.is_booked:
        slot.is_booked = True
        slot.occupied_by = request.user
        slot.save()

        messages.success(request, 'Slot occupied successfully.')
    else:
        messages.error(request, 'Slot already occupied or booked.')

    return redirect('home')

def get_slot_price(parking_area, slot_number):
    if slot_number % 3 == 1:
        return parking_area.pricelvl1
    elif slot_number % 3 == 2:
        return parking_area.pricelvl2
    else:
        return parking_area.pricelvl3


@login_required(login_url='login')
@permission_required('park.add_foundobject', raise_exception=True)
def add_found_object(request):
    accepted_image_formats = ".jpg, .png, .gif, .bmp, .tiff, .svg, .webp, .raw, .psd, .ai"
    parkings = ParkingArea.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        date_found = request.POST.get('date')
        parking_area_name = request.POST.get('parking')

        try:
            parking_area = ParkingArea.objects.get(name=parking_area_name)
            FoundObject.objects.create(
                name=name,
                description=description,
                image=image,
                date_found=date_found,
                parking_area=parking_area
            )
            messages.success(request, 'The object has been successfully added!')
            return redirect('found_objects')
        except ParkingArea.DoesNotExist:
            messages.error(request, 'Invalid parking area selected.')

    is_parking_manager = is_member(request.user, 'ParkingManager')
    is_user = is_member(request.user, 'User')
    context = {
        
        'is_parking_manager':is_parking_manager,
        'is_user':is_user,
        'accepted_image_formats': accepted_image_formats,
        'parkings': parkings,
    }
    return render(request, 'park/add_found_object.html', context)

@login_required(login_url='login')
def lost_object_request_view(request):
    accepted_image_formats = ".jpg, .png, .gif, .bmp, .tiff, .svg, .webp, .raw, .psd, .ai"
    parkings = ParkingArea.objects.all()
   
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        date_lost = request.POST.get('date')
        description = request.POST.get('description')
        user = request.user
        parking_area_name = request.POST.get('parking')

        try:
            parking_area = ParkingArea.objects.get(name=parking_area_name)
            LostRequest.objects.create(
                date=date_lost,
                description=description,
                user=user,
                parking_area=parking_area,
                photo=photo
            )
            messages.success(request, 'Your request has been successfully sent!')
            return redirect('found_objects')
        except ParkingArea.DoesNotExist:
            messages.error(request, 'Invalid parking area selected.')

    is_parking_manager = is_member(request.user, 'ParkingManager')
    is_user = is_member(request.user, 'User')
    context = {
        
        'is_parking_manager':is_parking_manager,
        'is_user':is_user,
        'accepted_image_formats': accepted_image_formats,
        'parkings': parkings,
    }
    return render(request, 'park/lost_object_request_form.html', context)

@login_required(login_url='login')
def my_lost_requests(request):
    lost_requests = LostRequest.objects.filter(user=request.user)
    responded=LostRequest.objects.filter(is_responded=True,user=request.user).count()
    if responded <= 0:
        theNumber=False
    else:
        theNumber=True    
    is_parking_manager = is_member(request.user, 'ParkingManager')
    is_user = is_member(request.user, 'User')
    context = {
        
        'is_parking_manager':is_parking_manager,
        'is_user':is_user,
        'lost_requests': lost_requests,
        'theNumber':theNumber}
    return render(request, 'park/my_lost.html',context)

@user_passes_test(lambda u: u.groups.filter(name='ParkingManager').exists())
def respond_to_lost_request(request, pk):
    lost_request = get_object_or_404(LostRequest, pk=pk)
    if request.method == 'POST':
        response = request.POST.get('response')
        lost_request.response = response
        lost_request.is_responded = True
        lost_request.save()
        return redirect('found_objects')
    is_parking_manager = is_member(request.user, 'ParkingManager')
    is_user = is_member(request.user, 'User')
    context = {
        
        'is_parking_manager':is_parking_manager,
        'is_user':is_user,
        'lost_request': lost_request,
    }
    return render(request, 'park/lost_object_response_form.html', context)

@permission_required('park.delete_foundobject', raise_exception=True)
def delete_found_object(request, pk):
    found_object = get_object_or_404(FoundObject, pk=pk)
    found_object.delete()
    messages.success(request, 'Found object has been successfully deleted.')
    return redirect('found_objects')

@login_required(login_url='login')
def found_objects(request):
    user = request.user    
    objects = FoundObject.objects.all()
    is_parking_manager = is_member(user, 'ParkingManager')
    is_user = is_member(user, 'User')
    lost_object_requests = LostRequest.objects.all().order_by('-date')
    responded=LostRequest.objects.filter(is_responded=True,user=request.user).count()
    if responded <= 0:
        theNumber=False
    else:
        theNumber=True    
    
    lost_requests = LostRequest.objects.filter(user=user)
    context = {
        'objects': objects,
        'is_parking_manager': is_parking_manager,
        'is_user': is_user,
        'lost_object_requests': lost_object_requests,
        'lost_requests': lost_requests,
        'theNumber':theNumber,
    }
    return render(request, 'park/found_objects.html', context)

@permission_required('park.delete_lostrequest', raise_exception=True)
def delete_lost_request(request, pk):
    lost_request = get_object_or_404(LostRequest, pk=pk)
    lost_request.delete()
    messages.success(request, 'Lost request has been successfully deleted.')
    return redirect('found_objects')

def slot_data(request, parking_area_id):
    parking = get_object_or_404(ParkingArea, id=parking_area_id)
    slots = Slot.objects.filter(area=parking)
    are_booked=Slot.objects.filter(area=parking, is_booked=True).count()
    libre = (parking.occupancy) - are_booked
    check_expired_reservations()
    slot_data = [
        {
            'slot_number': slot.slot_number,
            'is_booked': slot.is_booked,
            'status': slot.status,
        }
        for slot in slots
    ]
    return JsonResponse({'slots': slot_data, 'libre': libre})

