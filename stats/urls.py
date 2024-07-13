from django.urls import path
from . import views

urlpatterns = [
    path('statistics/', views.statistics_view, name='statistics'),
    path('contact/', views.contact_us, name='contact'),
    path('notif/', views.notifications, name='notif'),
    path('about/', views.about, name='about'),
    path('calendar/', views.calendar, name='calendar'),
    
    
]