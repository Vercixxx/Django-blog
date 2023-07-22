from django.shortcuts import render, get_object_or_404

# Posts
from posts.models import Post 
from comments.models import Comment
from comments.models import Posts_comments

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