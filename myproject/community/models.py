from django.db import models
from home.models import CustomUser
from tinymce.models import HTMLField

class Post(models.Model):
    type = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(CustomUser, related_name='written_posts', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
