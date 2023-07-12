from django.db import models
from posts.models import Post

# Create your models here.

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.TextField(default = "User")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    likes = models.IntegerField(default=0)
    content = models.TextField()

    class Meta:
        db_table = 'Comment'
        
        
class Posts_comments(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, to_field='id')

    combined_key = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.combined_key = f'{self.post_id_id}-{self.comment_id_id}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.combined_key
    
    class Meta:
        db_table = 'Posts_comments'