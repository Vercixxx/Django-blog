from django.contrib import admin

# Register your models here.
from .models import Comment,Posts_comments

admin.site.register(Comment)
admin.site.register(Posts_comments)