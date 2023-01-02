from django.urls import path
from adminuser.views import *
from django.contrib.auth import views as authentication_view
# from django.views import generic

app_name = 'adminuser'

urlpatterns = [
    
    path('',home, name="home"),
    path('viewuser/',viewuser, name="viewuser"),
    path('SignUp/',SignUp.as_view(), name="SignUp"),
    # path('login/', authentication_view.LoginView.as_view(template_name="login.html",authentication_form=CustomAuthForm), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',authentication_view.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path('noti/', Craetenotification.as_view(), name='noti'),
    path('notipageing/', NotificationList.as_view(), name='notipageing'),
]
