from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User as One

# Create your models here.

class User(AbstractUser):
    
    email=models.EmailField(max_length=100,unique=True,null=True)
    phone_number = models.IntegerField(unique=True,null=True)
    photo = models.ImageField(upload_to='user_images/',default="images/avatar.png")
    bio=models.CharField(null=True,blank=True,max_length=250)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.username
    



