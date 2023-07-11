from django.db import models


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.TextField(default = "User")
    title = models.TextField()
    content = models.TextField()
    views = models.IntegerField()
    comments = models.IntegerField()