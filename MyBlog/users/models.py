from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):

#  default='default_profile_pic.png'
    # My fields
    profile_pic = models.ImageField(null=True, 
                                    blank=True, 
                                    upload_to="images/users_prof_img/",
                                    default="images/users_prof_img/default_profile_pic.png")
    user_desc = models.TextField(max_length=250, default='Default profile description')
    
    # User rank
    RANK_CHOICES = (
        ('Newbie', 'Newbie'),
        ('Junior', 'Junior'),
        ('Member', 'Member'),
        ('SeniorMember', 'SeniorMember'),
        ('Veteran', 'Veteran'),
        ('Expert', 'Expert'),
        ('Guru', 'Guru'),
        ('Moderator', 'Moderator'),
        ('Administrator', 'Administrator'),
        )
    
    user_rank = models.CharField(
        max_length=20,
        choices=RANK_CHOICES,
        default='newbie'
    )
    
    def __str__(self):
        return self.username