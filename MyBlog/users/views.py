from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from functools import wraps
from django.http import HttpResponse

# auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import password_validation, update_session_auth_hash
from django.contrib.auth.models import User
from .forms import RegisterForm

# Captcha
from .forms import LoginForm

# secret_data
from .import_data import json_data

# Email conf
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def user_not_authenticated(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("Access denied. You don't have permission to access this page.", status=403)
        else:
            return view_func(request, *args, **kwargs)
    return wrapped_view

def activate_account(request, uibd64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uibd64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, f'Account has been activated succesfully, you can now log in')
        return redirect('login_view')
    
    else:
        messages.error(request, f'Activation link is invalid')
    
    return redirect('home_view')

def account_activation_message(request, user, to_mail):
    mail_subject = "Activate your user account"
    message = render_to_string("user/template_active_account.html",{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
        
        })
    
    email = EmailMessage(mail_subject, message, to=[to_mail])
    if email.send():
        message = f"Dear <b>{user}</b>, link for account activation has been sent to \
                    <b>{to_mail}</b>, please check your email to activate the account! (check spam folder also)"
        return messages.warning(request, mark_safe(message))
    else:
        mesasge = f"An error occured when sending email to <b>{to_mail}</b>, check if you typed correct email."
        return messages.error(request, mark_safe(message))
    
@user_not_authenticated
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
            
            # Setting account state to not active, waiting for email confirmation
            user.is_active = False
            user.save()
            account_activation_message(request, user, email)
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
    lf = LoginForm(request.POST)
    
    output_data = {
        'captcha':lf,
        }
            
    if request.method == 'POST':
        # if Captcha is valid
        if lf.is_valid():
            
            # Logging logic ========================
            username = request.POST["username"]
            password = request.POST["password"]
            
            user = authenticate(request, username=username, password=password)
            
            
            if user is not None:
                login(request, user)
                return redirect('home_view')
            else:
                messages.info(request, "Wrong username or password")
                return redirect('login_view')
            # Logging logic ========================
            
            
        else:
            # If captcha not vaild
            messages.info(request, 'Captcha error, try again')
            return redirect('login_view')
        
    
    else:
        return render(request, 'user/login.html', output_data)
    
    
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
            
            # check if username is unique
            if new_username != user.username:
                if User.objects.filter(username=new_username).exists():
                    messages.info(request, 'Username already exist!')
                else:
                    user.username = new_username
            

            # Setting new email
            if new_email != user.email:
                user.email = new_email
            
            # New password logic:
            if len(new_password1) > 0:
                if new_password1 == new_password2:
                    
                    validated_pass = is_password_valid(new_password1)
                    
                    if validated_pass is True:
                        user.set_password(new_password1)
                        update_session_auth_hash(request, user)
                        messages.info(request, 'Password changed sucesfully!' )
                    else:
                        output = ''.join(validated_pass)
                        messages.info(request, output )
                
                else:
                    messages.info(request, "Passwords are different" )
                    

            
            user.save()

            return redirect('user_account')
        
        return render(request, 'user/user_account.html')
    
def is_password_valid(new_password1):
    try:
        password_validation.validate_password(new_password1)
        return True
    except password_validation.ValidationError as e:
        return str(e)
    
    
