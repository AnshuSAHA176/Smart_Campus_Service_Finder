from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .cutom_manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
   email = models.EmailField(verbose_name="email address",
        max_length=255,
        unique=True,)
   is_active = models.BooleanField(default=True)

   is_staff = models.BooleanField(default= False)
   is_superuser = models.BooleanField(default= False)
   objects = CustomUserManager()

   username=None

   USERNAME_FIELD = 'email'


   REQUIRED_FIELDS = []

   def __str__(self):
      return f"{self.email}"


