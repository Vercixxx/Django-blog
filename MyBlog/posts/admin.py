from django.contrib import admin

# Register your models here.
from .models import Post, PostsThumbs

admin.site.register(Post)
admin.site.register(PostsThumbs)