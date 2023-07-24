from django.db import models
from django.utils import timezone

from posts.models import Post



class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    
    author = models.TextField(default = "User")
    posted_date = models.DateTimeField(default=timezone.now)
    
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    content = models.TextField()

    class Meta:
        db_table = 'Comment'
        
    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)  # Wywołanie oryginalnej metody save, która zapisuje obiekt w bazie danych

            # Tworzenie obiektu Posts_comments
            post_comment = Posts_comments(post_id=self.post_id, comment_id=self)
            post_comment.save()
            
        
class Posts_comments(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, to_field='id')

    combined_key = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.combined_key = f'{self.post_id_id}-{self.comment_id_id}'
        super().save(*args, **kwargs)
        
        # Add 1 to comments counter in post
        post = self.post_id
        post.comments = post.comment_set.count()  # Aktualizacja liczby komentarzy
        post.save()
        

    def __str__(self):
        return self.combined_key
    
    class Meta:
        db_table = 'Posts_comments'