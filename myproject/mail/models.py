from django.db import models
from home.models import CustomUser

# Create your models here.
class Mail(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_mails', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_mails', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

