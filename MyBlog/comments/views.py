from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404


# Posts
from posts.models import Post 
from posts.models import PostsThumbs 
from .models import Comment
from .models import Posts_comments

# User
from django.contrib.auth.models import User

# Adding comments
def add_comment(request, post_id):
    referer = request.META.get('HTTP_REFERER')
    
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)

        
        comment_content = request.POST.get("comment_content")

        Comment.objects.create(
            author=request.user.username,
            post_id=post,
            content=comment_content
                )
        
        
    else:
        raise Http404('Access denied: You must be logged in to add a comment.')

    return redirect(referer)