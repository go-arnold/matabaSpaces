from django.shortcuts import render,redirect
from park.models import ParkingArea, TheCity, Slot,FoundObject
from django.db.models import Count
from django.contrib import messages
from .models import Message_Contact, Notification


def statistics_view(request):
    # Line Chart Data: Percentage of slots occupied per hour for each parking area
    try:
        parking_areas = ParkingArea.objects.all()
        villes=TheCity.objects.all().count()
        total_slots= Slot.objects.all().count()
        occupied_slots=Slot.objects.filter(status=True).count()
        booked=Slot.objects.filter(is_booked=True).count()
        allparks=ParkingArea.objects.all().count()
        occupied_percent=(occupied_slots/total_slots)*100
        occupied_percent=round(occupied_percent,2)
        book_percent=(booked/total_slots)*100
        book_percent=round(book_percent,2)
        avg_per_ville=round((allparks/villes),2)
        objects=FoundObject.objects.all().count()
        objects_park=round((objects/allparks),2)
    except(ZeroDivisionError):
        messages.error(request, 'Not sufficient data to show Statistics')
        return redirect('home')    
    
    
    
    line_chart_data = {
        'labels': [str(i) for i in range(1, 25)],  # Hours of the day
        'datasets': []
    }
    for parking_area in parking_areas:
        occupancy_data = [parking_area.occupancy for _ in range(24)]  # Mock data, replace with actual, c'est pour prendre sasa les vraies donnees de occupancy
        line_chart_data['datasets'].append({
            'label': parking_area.name,
            'data': occupancy_data,
        })

    # Mixed Chart Data: Prices for each parking area
    mixed_chart_data = {
        'labels': [parking_area.name for parking_area in parking_areas],
        'datasets': [
            {
                'label': 'Standard',
                'type': 'bar',
                'data': [parking_area.pricelvl1 for parking_area in parking_areas]
            },
            {
                'label': 'Premium',
                'type': 'bar',
                'data': [parking_area.pricelvl2 for parking_area in parking_areas]
            },
            {
                'label': 'Discounted',
                'type': 'bar',
                'data': [parking_area.pricelvl3 for parking_area in parking_areas]
            },
            {
                'label': 'Average Price',
                'type': 'line',
                'data': [(parking_area.pricelvl1 + parking_area.pricelvl2 + parking_area.pricelvl3) / 3 for parking_area in parking_areas]
            }
        ]
    }

    # Doughnut Chart Data: Number of parking areas per city
    cities = TheCity.objects.all()
    doughnut_chart_data = {
        'labels': [city.name for city in cities],
        'datasets': [{
            'data': [ParkingArea.objects.filter(city=city).count() for city in cities],
        }]
    }
    
    # Calculate number of parking areas per city and add to the context
    city_parking_counts = []
    for city in cities:
        city_parking_counts.append({
            'name': city.name,
            'nparks': ParkingArea.objects.filter(city=city).count()
        })

    context = {
        'line_chart_data': line_chart_data,
        'mixed_chart_data': mixed_chart_data,
        'doughnut_chart_data': doughnut_chart_data,
        'total_slots': total_slots,
        'booked': booked,
        'avg_per_ville': avg_per_ville,
        'avg_per_ville_percent': (1 / avg_per_ville) * 100,
        'book_percent': book_percent,
        'occupied_percent': occupied_percent,
        'allparks': allparks,
        'objects_park': objects_park,
        'objects_park_percent': (1 / objects_park),
        'objects': objects,
        'city_parking_counts': city_parking_counts, 
        
    }

    
    return render(request, 'stats/global_occupation.html', context)



def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        email = request.POST.get('email')

        if name and message and email:
            contact_message = Message_Contact(
                sender=name,
                body=message,
                email=email
            )
            contact_message.save()
            messages.success(request, 'Message sent successfully')
            return redirect('contact')  # Redirige pour éviter de renvoyer le formulaire en POST
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'contact.html')

def notifications(request):
    notifs=Notification.objects.all()
    user=request.user
    context={
        'notifs':notifs,
        'user':user,
    }   
    return render(request,'stats/notifications.html',context)
def calendar(request):
    return render(request,'calendar.html',{})

def about(request):
    return render(request,'about.html',{})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

def custom_403_view(request, exception):
    return render(request, '403.html', status=403)

def custom_400_view(request, exception):
    return render(request, '400.html', status=400)


    