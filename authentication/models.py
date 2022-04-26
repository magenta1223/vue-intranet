from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser 
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser):
    username = models.EmailField(verbose_name = '이메일', unique=True)
    age = models.IntegerField()
    city = models.CharField(max_length=15)
    
    objects = UserManager()
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default= True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = ['age', 'city']


    def __str__(self):
        return self.username