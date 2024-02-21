from django.db import models
from home.models import CustomUser
from tinymce.models import HTMLField

class Post(models.Model):
    type = models.IntegerField(default=0)
    likes = models.ManyToManyField(CustomUser, blank=True, related_name='like_users')
    author = models.ForeignKey(CustomUser, related_name='written_posts', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='user_comment', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self',null=True,blank=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)