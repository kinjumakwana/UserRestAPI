from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be a staff'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be a superuser'
            )

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,max_length=255,blank=False)
    first_name = models.CharField('first name',max_length=150,blank=True)
    last_name = models.CharField('last name',max_length=150,blank=True)
    mobile= models.PositiveBigIntegerField('mobile',null=True,blank=True)
    address=models.CharField('address',max_length=150,blank=True)
    is_staff = models.BooleanField('staff status',default=False)
    is_active = models.BooleanField('active',default=True)
    is_admin     = models.BooleanField(default=False)
    is_superuser = models.BooleanField('superuser',default=False)
    # date_joined = models.DateTimeField('date joined',default=timezone.now)
  
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name+" "+self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Notification(models.Model):
    title = models.CharField(max_length=150,blank=True)
    body = models.CharField(max_length=150,blank=True)
