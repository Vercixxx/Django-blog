from django.db import models
from django.utils import timezone

class Technology(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/tech')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Technology'
        
class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    
    project_url = models.URLField(null=True)
    
    posted_date = models.DateTimeField(default=timezone.now)
    
    title = models.TextField()
    
    description = models.TextField()
    
    commits = models.IntegerField(default=0)
    
    branches = models.IntegerField(default=0)
    
    last_commits = models.TextField(default="----")
    
    status = models.IntegerField(default=0)
    
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    # Many to many relation
    technologies = models.ManyToManyField(Technology)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Projects'
        
        
