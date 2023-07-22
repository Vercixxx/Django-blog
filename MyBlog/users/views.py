from django.shortcuts import render, redirect

# auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



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
    return render(request, 'user/register.html', output)


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
        return render(request, 'user/login.html')
    
    
def logout_user(request):
    logout(request)
    messages.info(request, "Sucesfully logged out")
    return redirect('home_view')
 
 
@login_required(login_url='/user/login.html')
def user_account(request):

            
    
    if not request.user.is_authenticated:
        messages.info(request, 'Access denied, log in first!')
        return redirect('login_view')
    
    else:
        if request.method == 'POST':
            user_id = request.user.id
            
            new_username = request.POST["username"]
            new_email = request.POST['email']
            new_password1 = request.POST["password1"]
            new_password2 = request.POST["password2"]
            
            user = User.objects.get(id=user_id)
            user.username = new_username
            user.save()
            return redirect('user_account')
        
        return render(request, 'user/user_account.html')