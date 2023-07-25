from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse

# Posts
from posts.models import Post 
from comments.models import Comment
from comments.models import Posts_comments

from django.contrib.auth.decorators import login_required


def post_view(request, post_id):
    
    post = get_object_or_404(Post, id=post_id)
    
    comments = get_comments_for_post(post_id)
    
    
    # Adding 1 to views counter
    post.views += 1
    post.save()
    
    output = {
        'post': post,
        'comments':comments

    }
    return render(request, 'post/post.html', output)



def get_comments_for_post(post_id):
    # Extracing comments for post with id post_id
    comments = Comment.objects.filter(post_id=post_id)
    return comments


# Likes and dislikes handle


def like_clicked(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        
        print(f'Like clicked! Post ID: {post_id}, User ID: {user_id}')
        
    return HttpResponse()

def dislike_clicked(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')


        print(f'Like clicked! Post ID: {post_id}, User ID: {user_id}')

    return HttpResponse()


def add_post_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        title = request.POST.get("post_title")
        content = request.POST.get("post_content")
        
        Post.objects.create(author_id=user_id, title=title, content=content)
        
        return redirect('home_view')

    return render(request, 'blog/blog.html')


def delete_post_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.warning(request, "Post has been deleted")
        return redirect('home_view')
    return redirect('home_view')


def save_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        new_title = request.POST.get("post_title")
        new_content = request.POST.get("post_content")
        
        post.title = new_title
        post.content = new_content
        post.save()
        
        url = reverse('post_view', args=[post_id])
        
        return redirect(url)
    