from .forms import *
from .models import *
from userapi.serializers import *
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import generic
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from .forms import CustomAuthForm

# Create your views here.
def home(request):
    return render(request,'index.html')

class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('adminuser:login')
    template_name = 'sign_up.html'

# def login_view(request):
#     if request.method == 'POST':
#         form = CustomAuthForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('success')
#             else:
#                 form.add_error(None, "Invalid login credentials")
#     else:
#         form = CustomAuthForm()
#     return render(request, 'login.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

@login_required
def viewuser(request):
    user = request.user
    print(user)
    # all user data
    # userdata = User.objects.all()
    # print(userdata)
    userdata1 = User.objects.get(email=user)
    print(userdata1)
    # print(userdata.Address)
    # print(userdata.Contactno)
    # print(userdata.email)

    # context={'u':userdata} 
    context={'u':userdata1} 
    return render(request,"viewuser.html", context)

from django.db.models.signals import post_save
from django.dispatch import receiver
import firebase_admin
from firebase_admin import credentials, messaging
import os
from django.conf import settings

service_account_key_path = settings.SERVICE_ACCOUNT_KEY_PATH
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred)

@receiver(post_save, sender=User)
def user_saved(sender, instance, **kwargs):

# Define the notification payload:
  notification = messaging.Notification(title='New User added!', body='Welcome to New User!')

# Define the message:
  message = messaging.Message(notification=notification, topic='user')

# Send the message:
  response = messaging.send(message)

# Print the response to check for any errors:
  print(response)

class Craetenotification(generic.CreateView):
    form_class = NotificationForm
    template_name = 'notification.html'


def create_notification(request):
    form = NotificationForm(request.POST)
    if form.is_valid():
        notification = form.save()
        notification.send_notification()
        return redirect('success')
    else:
        return render(request, 'create_notification.html', {'form': form})

from django.dispatch import receiver
@receiver(post_save, sender=Notification)
def send_notification(sender, instance,**kwargs):
    
        title = instance.title
        body = instance.body

        notification = messaging.Notification(title=title, body=body)

        # Define the message:
        message = messaging.Message(notification=notification, topic='notification')

        # Send the message:
        response = messaging.send(message)

        # Print the response to check for any errors:
        print(response)

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import generics

class MyPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

from .mypagination import Mycustompagination

class NotificationList(generics.ListAPIView):
        queryset = Notification.objects.all()
        serializer_class = Notificationserializer
        pagination_class = Mycustompagination
        
# http://127.0.0.1:8000/adminuser/notipageing

