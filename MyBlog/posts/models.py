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
        
        
class PostsThumbs(models.Model):
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    
    
    
    @property
    def combined_key(self):
        return f'{self.user_id}-{self.post_id}'
    
    def save(self, *args, **kwargs):
        self.combined_key
        super().save(*args, **kwargs)   
    
    
    def __str__(self):
        return self.combined_key    
    
    class Meta:
        db_table = 'Posts_thumbs'
