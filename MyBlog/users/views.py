from django.shortcuts import render, redirect

# auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm


def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
  
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            
            password2 = form.cleaned_data.get('password2')
            if password != password2:
                return render(request, 'user/register.html', {'form': form, 'error_message': 'Passwords do not match.'})

            user = User.objects.create_user(username=username, email=email, password=password)

            messages.success(request, f"Account created for {username}")
            return redirect('home_view')
        

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error: {error}")
            form = RegisterForm()
        
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})



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