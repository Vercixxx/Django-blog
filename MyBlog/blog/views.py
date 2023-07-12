from django.shortcuts import render
from django.http import HttpResponse

# models
from posts.models import Post

# Create your views here.

def home_view(request):
    
    posts = Post.objects.all()
    
    return render(request, 'blog/index.html', {'posts':posts})


def about_view(request):
    return render(request, 'blog/about.html')