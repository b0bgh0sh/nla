from __future__ import unicode_literals
from django.db import models
from admin.models import Advisor
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Missing Required Email Field')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key = True, unique = True,
     serialize = False)
    name = models.CharField(max_length=30, blank = True)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

class Appointment(models.Model):
    id = models.AutoField(primary_key = True, unique = True, serialize = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete = models.CASCADE)
    time = models.DateTimeField()
