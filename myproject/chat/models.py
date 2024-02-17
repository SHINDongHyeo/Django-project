from django.db import models
from home.models import CustomUser

class ChatRoom(models.Model):
    title = models.CharField(max_length=255)
    current = models.IntegerField(default=1)
    limit = models.IntegerField(default=2)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
