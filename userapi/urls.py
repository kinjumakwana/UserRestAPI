from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

appname = "user"

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    # path('PDFview/', UserPDFView.as_view(), name='PDFview'),
    path('PDFview1/', UserPDFView1.as_view(), name='PDFview1'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('showuser/', show_user, name='showuser'),
    path('create-pdf/', pdf_report_create, name='create-pdf'),
    # path('userpdf/', GeneratePDFView.as_view(), name='userpdf'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('user-pdf/', UserDataViewSet.as_view(), name='user-pdf'),
    
]