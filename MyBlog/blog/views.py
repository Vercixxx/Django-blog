from django.shortcuts import render, redirect
from django.http import HttpResponse, request

from django.utils import timezone
from datetime import datetime


# models
from posts.models import Post 
from posts.models import PostsThumbs 
from comments.models import Comment 

# Pagination
from django.core.paginator import Paginator


def home_view(request): 

    # Pagination
    all_posts = Post.objects.order_by('-posted_date')
    p = Paginator(all_posts, 5)
    
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)    


    data = {'posts':page_obj, 
            'all_posts':all_posts, 
            'Comments':Comment, 
            'timezone':timezone, 
            'datetime':datetime,
            'thumbs':PostsThumbs,
            }
    
    return render(request, 'blog/blog.html', data)


 