from django.db import models


# Create your models 


#je cree les messages et contacts ici...
class Message_Contact(models.Model):
    
    sender= models.CharField(max_length=100)  
    email= models.EmailField(max_length=50)     
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)   
    

    def __str__(self):
        return f"A message from {self.sender.capitalize()}\n Whose Email address is {self.email} :\n\n {self.body} \n\n On the exact date {self.created_at} "
    
class Notification(models.Model):
    header = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to='notifications/', default="images/avatar.png")
    created_at = models.DateTimeField(auto_now_add=True)       
    
    def __str__(self):
        return self.body      
   