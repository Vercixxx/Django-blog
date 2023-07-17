from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils import timezone
from datetime import datetime

# register
from django.contrib import messages
from users.forms import UserRegisterForm

# models
from posts.models import Post 
from comments.models import Comment 



def home_view(request):

# register section:
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        
        if register_form.is_valid():
            register_form.save()
            
            
            register_username = register_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {register_username}!')
            # return redirect('home_view')
            
    else:
        register_form = UserRegisterForm()
    
    

    
    data = {'posts':Post.objects.all(), 
            'Comments':Comment, 
            'timezone':timezone, 
            'datetime':datetime,
            'register_form':register_form}
    
    return render(request, 'blog/blog.html', data)





