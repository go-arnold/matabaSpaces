from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('parking/<str:parking_area_id>/', views.parking, name="parking"),
    path('pricing/<str:pk>/', views.pricing, name="pricing"),
    
    path('data/', views.ldrdata, name="data"),
    path('found_objects/', views.found_objects, name='found_objects'),
    path('add_found_object/', views.add_found_object, name='add_found_object'),
    path('request_lost_object/', views.lost_object_request_view, name='request_lost_object'),
    path('my_lost_requests/', views.my_lost_requests, name='my_lost_requests'),
    path('respond_to_lost_request/<int:pk>/', views.respond_to_lost_request, name='respond_to_lost_request'),
    path('found_objects/delete/<int:pk>/', views.delete_found_object, name='delete_found_object'),
    path('lost_requests/delete/<int:pk>/', views.delete_lost_request, name='delete_lost_request'),
    path('slot_data/<str:parking_area_id>/', views.slot_data, name='slot_data'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
