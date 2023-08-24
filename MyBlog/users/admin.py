from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import MyUser
from .forms import UserAdminConf


class MyUserAdmin(admin.ModelAdmin):
    form = UserAdminConf
    list_display = ['username', 'email', 'is_active']
    
admin.site.register(MyUser, MyUserAdmin)