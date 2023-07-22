from django.shortcuts import render, get_object_or_404

# Posts
from posts.models import Post 
from comments.models import Comment 

def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    output = {
        'post': post,
    }
    return render(request, 'post/post.html', output)