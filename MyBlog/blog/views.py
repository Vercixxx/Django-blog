from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils import timezone
from datetime import datetime


# models
from posts.models import Post 
from comments.models import Comment 



def home_view(request):

    data = {'posts':Post.objects.all(), 
            'Comments':Comment, 
            'timezone':timezone, 
            'datetime':datetime,
            }
    
    return render(request, 'blog/blog.html', data)


