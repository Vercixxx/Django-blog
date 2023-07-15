from django.shortcuts import render
from django.http import HttpResponse

from django.utils import timezone
from datetime import datetime

# models
from posts.models import Post 
from comments.models import Comment 



def home_view(request):
    
    posts = Post.objects.all()
    
    return render(request, 'blog/blog.html', {'posts':posts, 'Comments':Comment, 'timezone':timezone, 'datetime':datetime})

