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

# DB
from django.db.models import Q

# Quotes
# from django.conf import settings
from django.templatetags.static import static
import os


def home_view(request): 
        
    searching = None
    all_posts = Post.objects.order_by('-posted_date')
    
    
    # Search bar logic:
    if request.method == 'POST'  and 'search_content' in request.POST:
        searching = request.POST['search_content']

        title = request.POST.get('checkbox_title') == 'on'
        content= request.POST.get('checkbox_content') == 'on'
        users = request.POST.get('checkbox_users') == 'on'

        filters = [
            Q(title__icontains=searching) if title else Q(),
            Q(content__icontains=searching) if content else Q(),
            Q(author__username__icontains=searching) if users else Q(),
        ]

        all_posts =  all_posts.filter(*filters)
        
	
	# Pagination
    p = Paginator(all_posts, 5)
    
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)    


    # Daily thoughts
    # dt = get_quotes()

    # print(dt)

    data = {'posts':page_obj, 
            'all_posts':all_posts[:6], 
            'Comments':Comment, 
            'timezone':timezone, 
            'datetime':datetime,
            'thumbs':PostsThumbs,
            'searched':searching
            }
    
    return render(request, 'blog/blog.html', data)

# def read_file_to_dict(file_path):
#     result_dict = {}

#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     for idx, line in enumerate(lines):
#         result_dict[idx] = line.strip()

#     return result_dict

# def get_quotes():
#     path = os.path.join(static('quotes/quotes.txt'))
#     data_dict = read_file_to_dict(path)
#     for key, value in data_dict.items():
#         print(key, value)

#     print(path)
