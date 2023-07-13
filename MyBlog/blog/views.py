from django.shortcuts import render
from django.http import HttpResponse

# models
from posts.models import Post 
from comments.models import Comment 



def home_view(request):
    
    posts = Post.objects.all()
    
    return render(request, 'blog/index.html', {'posts':posts, 'Comments':Comment})


def about_view(request):
    return render(request, 'blog/about.html')