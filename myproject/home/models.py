from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    point = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    notread = models.IntegerField(default=0)
    reported = models.IntegerField(default=0)
    profile = models.ImageField(upload_to='profile_images/', default='default_profile.jpg', blank=True)
