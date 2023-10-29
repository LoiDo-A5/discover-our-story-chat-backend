from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    is_using_social_avatar = models.BooleanField(default=False)
    social_avatar_hash = models.CharField(max_length=32, default='')
    birthday = models.DateField(null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    time_zone = models.CharField(max_length=50, default='Asia/Ho_Chi_Minh', blank=True)
