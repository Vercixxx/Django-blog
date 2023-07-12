from django.db import models


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.TextField(default = "User")
    title = models.TextField()
    content = models.TextField()
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        db_table = 'Post'