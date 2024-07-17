from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
#from django.contrib.auth.models import User
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site 
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from park.models import LostRequest
import re
from authentication.utils import is_member


#import authentication



User = get_user_model()

def activate(request,uidb64,token):
    User = get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None
        
        
    if user is not None and account_activation_token.check_token (user,token)  :
        user.is_active=True
        user.save()
        messages.success(request,f"Thanks {user.first_name}, you can now login ")
        return redirect('login')
    else:
        messages.error(request,"Sorry, we could not confirm your account")
        return redirect('register')     
    

def register(request):
    page='register'
    if request.method=='POST':
            first_name=request.POST.get('fname')
            last_name=request.POST.get('lname')
            email=request.POST.get('email')
            password=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
            phone=request.POST.get('phone')
            phone_pattern = re.compile(r'^(079|078|072|073)\d{7}$')
            if not phone_pattern.match(phone):
                messages.error(request, 'Invalid Rwandan Phone number !')
                return redirect('register')
            
            if password != pass2:
                messages.error(request,'The passwords do no match !!!')
                return redirect ('register')
            elif len(password) < 8:
                messages.error(request,'Password too short, Retry !')
                return redirect ('register')
            
            elif User.objects.filter(username=email):
                messages.error(request,'Email already registered !')
                return redirect ('register')
            
            # Vérification des critères du mot de passe
            if not re.search(r'[A-Z]', password):
                messages.error(request, 'Password must contain at least one uppercase letter!')
                return redirect('register')
            if not re.search(r'[a-z]', password):
                messages.error(request, 'Password must contain at least one lowercase letter!')
                return redirect('register')
            if not re.search(r'[0-9]', password):
                messages.error(request, 'Password must contain at least one digit!')
                return redirect('register')
            if not re.search(r'[\W_]', password):  # \W matches any non-word character, including special characters
                messages.error(request, 'Password must contain at least one special character!')
                return redirect('register') 
            if User.objects.filter(phone_number=phone).exists():
                messages.error(request, 'Phone number already registered!')
                return redirect('register')  
            user = User.objects.create_user(
                username=email,  
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False, 
                phone_number=phone                 
            )                        
            user.save()             
            
            #___________________________________________________________________________________            
            
            mail_subject="Activate your user account ! (: "
            message=render_to_string("authentication/activation.html",{
                'user': user.first_name,
                'domain':get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            }
            )
            lemail=EmailMessage(mail_subject,message,to=[user.email])
            if lemail.send():
                messages.success(request,f"Dear {user.first_name}, please go to your email '{user.email}' and  \
                                click on the activation link. You may need to check the span Folder ")
            else:
                messages.error(request, f"Unfortunately the message couldn't be sent to '{user.email}', check the spelling!!! ")
            
            #____________________________________________________________________________________
                      
            
    context={'page':page}
    return render(request,'authentication/login-register.html',context) 


def loginUser(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('pass1')
        try:
            user=User.objects.get(email=email)
            
        except User.DoesNotExist: 
            messages.error(request,"User does not exit, \n Incorrect email ") 
            
        user = authenticate(request,username=email,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        elif user is None  :
            messages.error(request,"Password incorrect ") 
                        
        else:
            messages.error(request,"Password incorrect")
         
    context={'page':page}    
    return render(request,'authentication/login-register.html',context)
  
@login_required   
def logoutUser(request):
    
    logout(request)
    return redirect ('login')

@login_required
def changeAll(request):
    user = request.user
    accepted_image_formats = ".jpg, .png, .gif, .bmp, .tiff, .svg, .webp, .raw, .psd, .ai"
    lost_object_requests = LostRequest.objects.all().order_by('-date')
    lost_requests = LostRequest.objects.filter(user=request.user)
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        bio=request.POST.get('bio')
        photo = request.FILES.get('photo')
        password = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        current = request.POST.get('current')
        if bio:
            user.bio=bio
            user.save()
        if not user.check_password(current):
            messages.error(request, 'Current password, INCORRECT !!!')
            return redirect('change')        
        
        if password != pass2:
            messages.error(request, 'The passwords do not match !!!')
            return redirect('change')
        
        if len(password) < 8:
            messages.error(request, 'Password too short, Retry !')
            return redirect('change')
        
        user.first_name = first_name
        user.last_name = last_name
        if photo:
            user.photo = photo
        
        user.set_password(password)
        user.save()
       
        
        messages.success(request, 'You have successfully updated your profile !')
        login(request, user)  
        return redirect('change')
    is_parking_manager = is_member(user, 'ParkingManager')
    is_user = is_member(user, 'User')
    context = {
       'user': request.user,
       'is_parking_manager':is_parking_manager,
       'is_user': is_user,
       'lost_requetes':lost_requests,
       'lost_object_requests':lost_object_requests,
       }
    return render(request, 'authentication/profile.html', context)
    


def reset(request):
    if request.method=='POST':
        email=request.POST.get("email")
        user=get_user_model().objects.filter(Q(email=email)).first()
        if user:            
            mail_subject="Reset Passord Request!"
            message=render_to_string("authentication/template-reset.html",{
                'user': user.first_name,
                'domain':get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            }
            )
            lemail=EmailMessage(mail_subject,message,to=[user.email])
            if lemail.send():
                messages.success(request,f"Dear {user.first_name.capitalize()},We have emailed you on «{user.email}» .  \
                                So, please go and follow the instructions.")
                return redirect('login')
            else:
                messages.error(request, f"Unfortunately the reset email message couldn't be sent to «{user.email}», check the spelling!!! ")
                return redirect('reset')
            
        else:
            messages.error(request,'Please enter your correct registered email !')
            return redirect('reset')    
    context={}
    return render (request,'authentication/reset.html',context)

def resetConfirm(request,uidb64,token):
    User = get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None
        
        
    if user is not None and account_activation_token.check_token (user,token)  :
        if request.method=='POST':
            
            password=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
            
            if password != pass2:
                messages.error(request,'The passwords do no match !!!')
                return redirect ('register')
            elif len(password) < 8:
                messages.error(request,'Password too short, Retry !')
                return redirect ('register')
            
            user.set_password(password)  
            user.save()                  
                    
            messages.success(request,f"Dear {user.first_name}, Your password has been changed successfully ")
            return redirect('login')
        
    else:
        messages.error(request,"Sorry, Invalid or expired Activation link ")
        return redirect('home')
    return render(request,'authentication/reset-confirm.html',{})
    
    

     
    
    
    
    