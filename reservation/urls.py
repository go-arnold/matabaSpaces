from django.urls import path
from . import views

urlpatterns = [
    path('selected/<str:pk>/', views.reserve_slot, name="reserve"),
    path('selected/<str:pk>/', views.selectSlot, name="select"),
]
