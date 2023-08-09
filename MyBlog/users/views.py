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
from .tokens import account_activation_token, recover_password_token
from django.urls import reverse


# UserPosts models
from posts.models import Post 
from posts.models import PostsThumbs 
from comments.models import Comment
from django.utils import timezone
from datetime import datetime

# DB
from django.db.models import Q


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
 
 
def update_password(request):
    
    if request.method == 'POST':
        previous_url = request.POST.get('previous_url')
        user_id = request.POST.get('user_id')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')

        user = User.objects.get(pk=user_id)

        # New password logic:
        if new_password1 == new_password2:
            
            validated_pass = is_password_valid(new_password1)
            
            if validated_pass:
                user.set_password(new_password1)
                messages.info(request, 'Password changed sucesfully!' )
                user.save()
                
                messages.success(request, f'Password sucesfully changed! You can log in')

                return redirect('login_view') 
                
            else:
                output = ''.join(validated_pass)
                messages.info(request, output )

                   
        else:
            messages.info(request, "Passwords are different" )
            return redirect(previous_url)
            
    else:
        return redirect(previous_url)
            
    
def password_recovery(request, uibd64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uibd64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and recover_password_token.check_token(user, token):

        link = request.session['recovery_link'] = reverse('password_recovery', args=[uibd64, token])

        context = {
            'uid': uibd64,
            'token': token,
            'user': user,
            'previous_url': link,
        }
        
        return render(request, 'user/password_recovery.html', context)
    
    else:
        messages.error(request, f'Link is invalid')
        return redirect('login_view')
    

def password_recovery_message(request, user, to_mail):
    mail_subject = "Password recovery"

    
    message = render_to_string("user/template_recover_password.html",{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': recover_password_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
        
        })
    
    email = EmailMessage(mail_subject, message, to=[to_mail])
    
    if email.send():
        message = f"Recovery mail has been sent to <b>{to_mail}</b>, check email box"
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


@user_not_authenticated
def login_view(request):
    lf = LoginForm(request.POST)
    
    output_data = {
        'captcha':lf,
        }
            
    if request.method == 'POST':
        # if Captcha is valid
        if lf.is_valid() and 'password_recovery_form' not in request.POST:
            
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
            
        elif 'password_recovery_form' in request.POST: 
            recovery_email = request.POST['email']
            
            # check if user exist in database
            if User.objects.filter(email=recovery_email).exists():
                user = User.objects.get(email=recovery_email)
                
                # calling funcions
                password_recovery_message(request, user, recovery_email)
                
                return redirect('login_view')
            else:
                messages.info(request, f'There isnt user registered on mail {recovery_email}')
                return redirect('login_view')
            
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
 
 
# @login_required(login_url='/user/login.html')
def user_account(request, username):
    user = User.objects.get(username=username)
    user_id = user.id
    
    posts = Post.objects.filter(author_id=user_id).order_by('-posted_date')
    
    data = {
        'user': user,
        'posts': posts, 
        'Comments':Comment, 
        'timezone':timezone, 
        'datetime':datetime,
        'thumbs':PostsThumbs,
    }
    
    
    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get("username")
        new_email = request.POST.get('email')
        new_password1 = request.POST.get("password1")
        new_password2 = request.POST.get("password2")

        # check if username is unique
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.info(request, 'Username already exist!')
            else:
                user.username = new_username
                messages.success(request, 'Username changed!')

        # Setting new email
        if new_email and new_email != user.email:
            messages.success(request, 'Email changed!')
            user.email = new_email

        # New password logic
        if new_password1:
            
            if new_password1 == new_password2:
                validated_pass = is_password_valid(new_password1)
                
                if validated_pass:
                    user.set_password(new_password1)
                    update_session_auth_hash(request, user)
                    messages.info(request, 'Password changed sucesfully!' )
                    
                else:
                    output = ''.join(validated_pass)
                    messages.info(request, output )
                    
            else:
                messages.info(request, "Passwords are different" )

        user.save()

        return redirect('user_account', username=new_username)

    else:
        return render(request, 'user/user_account.html', data)
    
    
def is_password_valid(new_password1):
    try:
        password_validation.validate_password(new_password1)
        return True
    except password_validation.ValidationError as e:
        return str(e)