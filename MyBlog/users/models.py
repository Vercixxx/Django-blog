from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):

    # My fields
    profile_pic = models.ImageField(null=True, blank=True)
    
    
    def __str__(self):
        return self.username