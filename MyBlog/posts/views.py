from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.urls import reverse

# Posts
from posts.models import Post 
from posts.models import PostsThumbs 
from comments.models import Comment
from comments.models import Posts_comments

# User
from django.contrib.auth import get_user_model

# json
from django.http import JsonResponse


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
@login_required(login_url='/user/login.html')
def like_clicked(request):
    User = get_user_model()
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        
        post = get_object_or_404(Post, id=post_id)
        
        condition = PostsThumbs.objects.filter(user_id=user_id, post_id=post_id).exists()



        if condition:
            # User clicked like or dislike in past (exist in database)
            thumb = PostsThumbs.objects.get(user_id=user_id, post_id=post_id)
            
            # check if user clicked like
            if thumb.like:
                # unlike post
                thumb.like = False
                thumb.save()
                
                post.likes -= 1
                post.save()
                
            elif thumb.dislike:
                # case when user clicked false in past in this post
                thumb.dislike = False
                thumb.like = True
                thumb.save()
                
                post.dislikes -= 1
                post.likes += 1
                post.save()
                
            else:
                thumb.like = True
                post.likes += 1
                
                thumb.save()
                post.save()
                
            
            return JsonResponse({'like_count': post.likes, 'dislike_count': post.dislikes}) 
                
            
        else:
            # user never clicked like or dislike
            # create relation user-postLikes
            PostsThumbs.objects.create(user_id=user, 
                                       post_id=post,
                                       like=True)
            # add one like to post like counter
            post.likes += 1
            post.save()
 
    return HttpResponse()

@login_required(login_url='/user/login.html')
def dislike_clicked(request):
    User = get_user_model()
    
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        
        post = get_object_or_404(Post, id=post_id)
        
        condition = PostsThumbs.objects.filter(user_id=user_id, post_id=post_id).exists()


        if condition:
            # record exist in database
            thumb = PostsThumbs.objects.get(user_id=user_id, post_id=post_id)
            
            # check if user clicked like
            if thumb.like:
                #if like was pressed
                thumb.like = False
                thumb.dislike = True
                thumb.save()
                
                post.likes -= 1
                post.dislikes +=1
                post.save()
                
            elif thumb.dislike:
                # if disliked was pressed
                thumb.dislike = False
                thumb.save()
                
                post.dislikes -= 1
                post.save()
                
            else:
                # if none of option was pressed
                thumb.dislike = True
                thumb.save()
                
                post.dislikes += 1
                post.save()
                
            
            return JsonResponse({'like_count': post.likes, 'dislike_count': post.dislikes}) 
        else:
            # when user never clicked like or dislike
            PostsThumbs.objects.create(user_id=user, 
                                       post_id=post,
                                       dislike=True)
            # add one like to post like counter
            post.dislikes += 1
            post.save()
        
    
    return HttpResponse()


def get_like_dislike_counts(request):
    if request.method == 'GET':
        post_id = request.GET.get('post_id')
        post = Post.objects.get(pk=post_id)
        like_count = post.likes
        dislike_count = post.dislikes
        return JsonResponse({'like_count': like_count, 'dislike_count': dislike_count})


def add_post_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        title = request.POST.get("post_title")
        content = request.POST.get("post_content")
        
        Post.objects.create(author_id=user_id, title=title, content=content)
        
        return redirect('home_view')

    return render(request, 'blog/blog.html')

@login_required(login_url='/user/login.html')
def delete_post_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.warning(request, "Post has been deleted")
        return redirect('home_view')
    return redirect('home_view')

@login_required(login_url='/user/login.html')
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
    