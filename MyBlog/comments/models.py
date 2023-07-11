from django.db import models
from posts.models import Post

# Create your models here.

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.TextField(default = "User")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    likes = models.IntegerField()
    content = models.TextField()

    class Meta:
        db_table = 'Comment'
        
        
class Posts_comments(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, to_field='id')
    
    class Meta:
        db_table = 'Posts_comments'