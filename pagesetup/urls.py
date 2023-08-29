from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name = 'index'),
    path('login' , views.login_page , name='login'),
    path('register' , views.register_page , name='register'),
    path('logout' , views.logout_page , name='logout'),
    path('settings',views.settings,name='settings'),
    path('post',views.post,name='post'),
    path('profile',views.profile,name='profile'),
    path('oprofile/<id>',views.oprofile,name='oprofile'),
    path('like-post/<id>',views.like_post,name='like-post'),
]
