from io import BytesIO
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from xhtml2pdf import pisa
from rest_framework import views
from drf_pdf.response import PDFResponse
from drf_pdf.renderer import PDFRenderer
from rest_framework import generics, serializers
from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from wkhtmltopdf.views import PDFTemplateResponse
# from easy_pdf.rendering import render_to_pdf_response
from rest_framework.views import APIView
# import pypdf2
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import json

# Create your views here.
# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

from django.template.loader import get_template
from xhtml2pdf import pisa

def pdf_report_create(request):
    # user = User.objects.all()
    # user=User.objects.get(id=id)
    user=request.user

    print(user)
    print(type(user))

    template_path = 'user_pdf.html'

    context = {'user': user}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="user_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class UserPDFView1(APIView):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # Get user data from the request
        user_data = request.user
        print(user_data)

        input_type = type(user_data)
        print(input_type)
        # serializer = UserProfileSerializer(user_data)
       
        # Render the PDF template with the user data
        template = get_template('user_pdf.html')
        # data = json.loads(serializer)
        context = {'user': user_data}

        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="user_report.pdf"'

        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
          return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

from rest_framework import serializers, viewsets

def generate_pdf(request, user_data):
    # Render the HTML template with the user data as context

    html = render_to_string('user_pdf.html', {'user': user_data})
    
    # Create a BytesIO object
    buffer = BytesIO()
    
    # Generate the PDF using xhtml2pdf
    pisa.pisaDocument(html, buffer)
    
    # Get the PDF as a bytes object
    pdf = buffer.getvalue()
    
    # Create an HTTP response with the PDF as the content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user_data.pdf"'
    
    return response

class UserDataViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args, **kwargs):
        # Deserialize the user data from the request body
        serializer = UserProfileSerializer(request.user)
        user_data = serializer.data
        
        # Generate the PDF using the user data
        response = generate_pdf(request, user_data)
        
        return response

