from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import MyUser
from .forms import UserAdminConf


class MyUserAdmin(admin.ModelAdmin):
    form = UserAdminConf
    list_display = ['username', 'email', 'is_active']
    
    
    
# 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'profile_pic'

# User = get_user_model()
# admin.site.register(User)


admin.site.register(MyUser, MyUserAdmin)