from django.shortcuts import render, redirect
from django.http import HttpResponse

# auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.forms import UserRegisterForm

def register_view(request):

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        
        if register_form.is_valid():
            register_form.save()
            
            register_username = register_form.cleaned_data.get('username')
            
            messages.success(request, f'Account created for {register_username}!')
            return redirect('home_view') 
            
    else:
        register_form = UserRegisterForm()
        
    output = {
        'register_form':register_form,
    }    
    return render(request, 'user_form/register.html', output)


def login_view(request):
    if request.method == 'POST':
        
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home_view')
        else:
            messages.info(request, "Wrong username or password")
            return redirect('login_view')
    else:
        return render(request, 'user_form/login.html')