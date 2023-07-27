from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=timezone.now)
    
    title = models.TextField()
    content = models.TextField()
    
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        db_table = 'Post'