from django.shortcuts import render, redirect
from django.http import HttpResponse

# register
from django.contrib import messages
from users.forms import UserRegisterForm

# Create your views here.
def register_view(request):
    
# register section:
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
    return render(request, 'user_form/login.html')