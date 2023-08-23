from django.db import models
from django.utils import timezone


class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    
    posted_date = models.DateTimeField(default=timezone.now)
    
    title = models.TextField()
    content = models.TextField()
    
    status = models.IntegerField(default=0)
    
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        db_table = 'Projects'
        