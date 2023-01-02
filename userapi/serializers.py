from rest_framework import serializers
from adminuser.models import User,Notification
# from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from account.utils import Util
from django.contrib.auth import get_user_model
from rest_framework import serializers
# from drf_pdf import PDFSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email','mobile','address','password', 'password2']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = get_user_model()
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['id','first_name', 'last_name', 'email','mobile','address']

class Notificationserializer(serializers.ModelSerializer):
  class Meta:
    model = Notification
    fields = ['title','body']

