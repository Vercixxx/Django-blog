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

from django.conf import settings
from django.conf.urls.static import static

from blog import views as blog_views
from users import views as users_views
from posts import views as posts_views
from comments import views as comments_views
from cv import views as cv_views

app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # my sites
    path('', blog_views.home_view, name='home_view'),
    path('register/', users_views.register_view, name='register_view'),
    
    # mail when register
    path('activate/<uibd64>/<token>', users_views.activate_account, name='activate_account'),
    
    # Password recovery
    path('password_recovery/<uibd64>/<token>', users_views.password_recovery, name='password_recovery'),
    path('update_password/', users_views.update_password, name='update_password'),
    
    path('login/', users_views.login_view, name='login_view'),
    path('logout_user', users_views.logout_user, name="logout_user"),
    path('user/<str:username>/', users_views.user_account, name="user_account"),    

    
    # post
    path('post/<int:post_id>/', posts_views.post_view, name="post_view"),   
    path('add_post/', posts_views.add_post_view, name='add_post_view'),
    path('delete_post/<int:post_id>/', posts_views.delete_post_view, name='delete_post_view'),
    path('save_post/<int:post_id>/', posts_views.save_post, name='save_post'),

    # Adding comment to post
    path('add_comment/<int:post_id>/', comments_views.add_comment, name='add_comment'),
    
    # Deleting comment
    path('delete_comment/<int:comment_id>/', comments_views.delete_comment, name='delete_comment'),

    
    # Post likes / disklikes
    path('like_clicked/', posts_views.like_clicked, name='like_clicked'),
    path('dislike_clicked/', posts_views.dislike_clicked, name='dislike_clicked'),  
    path('get_like_dislike_counts/', posts_views.get_like_dislike_counts, name='get_like_dislike_counts'),
    
    # CV
    path('cv/', cv_views.cv_view, name='cv_view'),
    
    # Contact me
    path('contact_me_message/', cv_views.contact_me_message, name='contact_me_message'),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# Admin configureables
admin.site.site_header = "Chris Admin site"
admin.site.site_title = "Admin"
admin.site.index_title = "Welcome on Admin site! ^_^"
