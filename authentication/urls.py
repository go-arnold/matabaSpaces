from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutUser, name="logout"),  
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
   
    path('reset/', views.reset, name="reset"),
    path('reset-confim/<uidb64>/<token>', views.resetConfirm, name='reset-confirm'),
    path('change/', views.changeAll, name="change"),
    
  
    
    
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)