
from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    desc = models.TextField(null=True, blank=True, verbose_name="描述")
    picture = models.CharField(max_length=20,default="default.png")
