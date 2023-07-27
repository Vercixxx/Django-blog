"""
URL configuration for MyBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog import views as blog_views
from users import views as users_views
from posts import views as posts_views

app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # my sites
    path('', blog_views.home_view, name='home_view'),
    path('register/', users_views.register_view, name='register_view'),
    path('login/', users_views.login_view, name='login_view'),
    path('logout_user', users_views.logout_user, name="logout_user"),
    path('user/', users_views.user_account, name="user_account"),    
    
    # post
    path('post/<int:post_id>/', posts_views.post_view, name="post_view"),   
    path('add_post/', posts_views.add_post_view, name='add_post_view'),
    path('delete_post/<int:post_id>/', posts_views.delete_post_view, name='delete_post_view'),
    path('save_post/<int:post_id>/', posts_views.save_post, name='save_post'),

    
    # Post likes / disklikes
    path('like_clicked/', posts_views.like_clicked, name='like_clicked'),
    path('dislike_clicked/', posts_views.dislike_clicked, name='dislike_clicked'),  
    
    
]

# Admin configureables
admin.site.site_header = "Chris Admin site"
admin.site.site_title = "Admin"
admin.site.index_title = "Welcome on Admin site! ^_^"
